from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()


# Initialize the ApifyClient with your API token
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

client = ApifyClient(os.getenv("APIFY_API_KEY"))


def fatch_linkedin_job(search_query: str, location: str = 'Bulgaria', row: int = 30):
    """
    Fetch job listings from LinkedIn using Apify Actor.

    Parameters
    ----------
    search_query : str
        The job title or keywords to search for (e.g., "Software Engineer").
    location : str, optional
        The location to search jobs in (default is 'Bulgaria').
    row : int, optional
        Number of jobs to fetch (default is 50).

    Returns
    -------
    list[dict]
        A list of job postings where each job is represented as a dictionary.
    """
    run_input = {
        "title": search_query,
        "location": location,
        "rows": row,
        # "experienceLevel": "all",
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }

    # Run the LinkedIn Actor
    run = client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)

    # Fetch job results from the dataset
    jobs = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    return jobs


def fatch_glassdoor_job(search_query: str, location: str = 'Bulgaria', row: int = 30):
    """
    Fetch job listings from Glassdoor using Apify Actor.

    Parameters
    ----------
    search_query : str
        The job title or keywords to search for (e.g., "Data Scientist").
    location : str, optional
        The location to search jobs in (default is 'Bulgaria').
    row : int, optional
        Number of jobs to fetch (default is 30).

    Returns
    -------
    list[dict]
        A list of job postings where each job is represented as a dictionary.
    """
    run_input = {
        "keyword": search_query,
        "maxItems": row,
        "location": location,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        },
    }

    # Run the Glassdoor Actor
    run = client.actor("t2FNNV3J6mvckgV2g").call(run_input=run_input)

    # Fetch job results from the dataset
    jobs = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    return jobs
