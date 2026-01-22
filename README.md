# 💼 AI Job Recommender (Streamlit App)

An AI-powered job aggregation and recommendation system built with **Streamlit**.  
This app fetches job listings from **LinkedIn** and **Glassdoor**, normalizes them into a common format, removes duplicates, and displays them in a clean interactive dashboard.

---

## 🚀 Features

- 🔍 Fetch jobs from **LinkedIn** and **Glassdoor**
- 🧹 Normalize job data from different sources
- ❌ Remove duplicate job listings automatically
- 📊 Interactive Streamlit dashboard
- 🎛️ Filter jobs by:
  - Source (LinkedIn / Glassdoor)
  - Remote / On-site
- 🔃 Sort jobs by:
  - Date
  - Title
  - Company
- 📥 Export job results to **CSV**
- 🤖 AI Ranking (placeholder for future enhancement)

## 📂 Project Structure

```text
.
├── app.py                     # Main Streamlit app
├── src/
│   ├── job_search.py           # LinkedIn & Glassdoor fetch functions
│   ├── helper.py               # (Optional) AI / PDF / utility helpers
├── requirements.txt
├── README.md

```

## Clone repro

``` clone
git clone https://github.com/Ahmed2797/AI-Power-Job-Recommander-System.git

cd ai-job-recommender

```

## Environment setup

``` env
uv init
uv venv
uv add -r requirements.txt

python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt
streamlit run app.py
http://localhost:8501


```

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit**
- **Pandas**
- **Apify Actors** (for scraping Glassdoor / LinkedIn)
- **Custom Python modules**

---
