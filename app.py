import streamlit as st
import pandas as pd
from typing import List, Dict
from datetime import datetime
from src.job_search import fatch_glassdoor_job, fatch_linkedin_job
from src.helper import extract_text_from_pdf, ask_openai

# -------------------------------
# Utility Functions
# -------------------------------

def normalize_job_data(jobs: List[Dict], source: str) -> List[Dict]:
    """Normalize job data from different sources to a common format"""
    normalized_jobs = []
    
    for job in jobs:
        normalized = {
            "title": job.get("title") or job.get("jobTitle") or "N/A",
            "company": job.get("companyName") or job.get("company") or "N/A",
            "location": job.get("location") or "N/A",
            "salary": job.get("salary") or job.get("salaryRange") or "Not specified",
            "link": job.get("link") or job.get("jobUrl") or "#",
            "source": source,
            "date_posted": job.get("datePosted") or datetime.now().strftime("%Y-%m-%d"),
            "description": job.get("description") or job.get("summary") or "",
            "remote": "Remote" if "remote" in str(job.get("location", "")).lower() else "On-site/Hybrid"
        }
        normalized_jobs.append(normalized)
    
    return normalized_jobs

def remove_duplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    """Remove duplicate jobs based on title and company"""
    seen = set()
    unique_jobs = []
    
    for job in jobs:
        identifier = (job["title"].lower(), job["company"].lower())
        if identifier not in seen:
            seen.add(identifier)
            unique_jobs.append(job)
    
    return unique_jobs

# -------------------------------
# Session State
# -------------------------------
if 'all_jobs' not in st.session_state:
    st.session_state.all_jobs = []
if 'fetch_completed' not in st.session_state:
    st.session_state.fetch_completed = False

# -------------------------------
# Page Layout
# -------------------------------
st.set_page_config(page_title="AI Job Recommender", layout="wide", page_icon="💼")
st.title("💼 AI Job Recommender")
st.markdown("Fetch jobs from LinkedIn & Glassdoor and rank them using AI")
st.divider()

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your resume..."):
        summary = ask_openai(f"Summarize this resume highlighting the skills, edcucation, and experience: \n\n{resume_text}",max_tokens=700)

    with st.spinner("Finding skill Gaps..."):
        gaps = ask_openai(f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities: \n\n{resume_text}", max_tokens=700)

    with st.spinner("Creating Future Roadmap..."):
        roadmap = ask_openai(f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skill to learn, certification needed, industry exposure): \n\n{resume_text}", max_tokens=700)
    
    # Display nicely formatted results
    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully!")

# -------------------------------
# Sidebar Filters
# -------------------------------
with st.sidebar:
    st.header("🔍 Filters")
    job_title = st.text_input("Job Title", value="")
    location = st.text_input("Location", value="Remote")
    
    st.subheader("Number of Jobs")
    col1, col2 = st.columns(2)
    with col1:
        rows_linkedin = st.number_input("LinkedIn", min_value=5, max_value=200, value=5, step=5)
    with col2:
        rows_glassdoor = st.number_input("Glassdoor", min_value=5, max_value=200, value=5, step=5)
    
    st.subheader("Platform Selection")
    fetch_linkedin = st.checkbox("Fetch LinkedIn Jobs", value=True)
    fetch_glassdoor = st.checkbox("Fetch Glassdoor Jobs", value=True)
    
    st.divider()
    st.subheader("Display Options")
    show_salary = st.checkbox("Show Salary", value=True)
    show_remote = st.checkbox("Show Remote Status", value=True)

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2 = st.tabs(["🔎 Fetch Jobs", "📊 Job Dashboard"])

with tab1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Fetch Jobs", type="primary", use_container_width=True):
            st.session_state.all_jobs = []

            # ----------------
            # Experience Level Input
            # ----------------
            experience_mapping = {
                "intern": "1",
                "fresher": "2",
                "entry": "2",
                "associate": "3",
                "mid": "4",
                "senior": "4",
                "director": "5",
                "executive": "5"
            }
            user_exp_input = st.sidebar.text_input(
                "Experience Level (intern, entry, mid, senior, director)", 
                value="entry"
            ).lower()
            experience_level = experience_mapping.get(user_exp_input, "2")  # default "2" if invalid

            
            if fetch_linkedin:
                with st.spinner(f"Fetching {rows_linkedin} jobs from LinkedIn..."):
                    try:
                        linkedin_jobs = fatch_linkedin_job(job_title, location, rows_linkedin)
                        normalized_linkedin = normalize_job_data(linkedin_jobs, "LinkedIn")
                        st.session_state.all_jobs.extend(normalized_linkedin)
                        st.success(f"✅ Fetched {len(linkedin_jobs)} jobs from LinkedIn")
                    except Exception as e:
                        st.error(f"❌ Error fetching LinkedIn jobs: {str(e)}")
            
            if fetch_glassdoor:
                with st.spinner(f"Fetching {rows_glassdoor} jobs from Glassdoor..."):
                    try:
                        glassdoor_jobs = fatch_glassdoor_job(job_title, location, rows_glassdoor)
                        normalized_glassdoor = normalize_job_data(glassdoor_jobs, "Glassdoor")
                        st.session_state.all_jobs.extend(normalized_glassdoor)
                        st.success(f"✅ Fetched {len(glassdoor_jobs)} jobs from Glassdoor")
                    except Exception as e:
                        st.error(f"❌ Error fetching Glassdoor jobs: {str(e)}")
            
            # Remove duplicates
            if st.session_state.all_jobs:
                st.session_state.all_jobs = remove_duplicate_jobs(st.session_state.all_jobs)
                st.session_state.fetch_completed = True
                st.balloons()
                
                # Show summary
                st.info(f"""
                **Summary:**
                - Total unique jobs: {len(st.session_state.all_jobs)}
                # - LinkedIn: {len([j for j in st.session_state.all_jobs if j['source'] == 'LinkedIn'])}
                # - Glassdoor: {len([j for j in st.session_state.all_jobs if j['source'] == 'Glassdoor'])}
                """)

with tab2:
    if st.session_state.all_jobs:
        st.subheader(f"📋 Job Results ({len(st.session_state.all_jobs)} jobs found)")
        
        df = pd.DataFrame(st.session_state.all_jobs)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            source_filter = st.multiselect(
                "Filter by Source",
                options=df['source'].unique(),
                default=df['source'].unique()
            )
            # pass
        with col2:
            remote_filter = st.multiselect(
                "Filter by Remote",
                options=df['remote'].unique(),
                default=df['remote'].unique()
            )
            # pass
        with col3:
            sort_by = st.selectbox(
                "Sort by",
                options=["Title", "Company"],
                index=0
            )
        
        # Apply filters
        filtered_df = df[
            (df['source'].isin(source_filter)) &
            (df['remote'].isin(remote_filter))
        ]
        filtered_df = df
        
        # Sort
        if sort_by == "Title":
            filtered_df = filtered_df.sort_values('title')
        else:
            filtered_df = filtered_df.sort_values('company')
        
        # Display jobs
        for idx, job in filtered_df.iterrows():
            with st.expander(f"**{job['title']}** at {job['company']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Location:** {job['location']}")
                    if show_remote:
                        st.markdown(f"**Remote:** {job['remote']}")
                    if show_salary and job['salary'] != "Not specified":
                        st.markdown(f"**Salary:** {job['salary']}")
                    st.markdown(f"**Source:** {job['source']}")
                    st.markdown(f"**Posted:** {job['date_posted']}")
                
                with col2:
                    st.markdown(f"[Apply Here]({job['link']})")
                
                if job['description']:
                    st.markdown("**Description:**")
                    st.markdown(job['description'][:300] + "..." if len(job['description']) > 300 else job['description'])
        
        # Export / Refresh / AI ranking
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        with col2:
            if st.button("🔄 Refresh Jobs"):
                st.session_state.all_jobs = []
                st.rerun()
        with col3:
            if st.button("🤖 Run AI Ranking", type="secondary"):
                st.info("🚀 AI Ranking feature coming soon!")
                # Example placeholder for AI pipeline:
                # st.session_state.all_jobs = ai_ranking_function(st.session_state.all_jobs)
    else:
        st.info("👈 Click 'Fetch Jobs' to start searching for opportunities!")

# Footer
st.divider()
st.caption("Made with ❤️ | AI Job Recommender v1.0")
