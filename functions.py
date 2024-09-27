import requests
from bs4 import BeautifulSoup, FeatureNotFound
import logging
from typing import List, Optional
from googlesearch import search

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_google_results(query: str, num_results: int = 10) -> List[str]:
    """
    Fetch the top 'n' Google search results URLs for a given query.

    Parameters
    ----------
    query : str
        The search query.
    num_results : int
        The number of top results to fetch. Default is 5.

    Returns
    -------
    List[str]
        A list of URLs from the top Google search results.

    Raises
    ------
    ValueError
        If the query is empty or num_results is less than 1.

    requests.RequestException
        For network-related errors.
    """
    if not query:
        raise ValueError("The search query must be a non-empty string.")
    if num_results < 1:
        raise ValueError("The number of results must be at least 1.")

    try:
        results = search(query=query, num=num_results, stop=num_results, pause=2) 
        logging.info(f"Successfully fetched Google search results for query: {query}")
        return list(results)
    except Exception as e:
        logging.error(
            f"An error occurred while fetching the search results for query: {query}",
            exc_info=True,
        )
        raise e


def fetch_webpage_content(url: str) -> str:
    """
    Fetch and parse content from a specified webpage URL.

    Parameters
    ----------
    url : str
        The URL of the webpage to be fetched and parsed.

    Returns
    -------
    str
        The textual content of the webpage.

    Raises
    ------
    ValueError
        If the URL is empty.

    requests.RequestException
        For network-related errors.

    bs4.FeatureNotFound
        If the parsing library is not found.
    """
    if not url:
        raise ValueError("The URL must be a non-empty string.")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        logging.info(f"Successfully fetched the webpage: {url}")
    except requests.RequestException as e:
        logging.error(
            f"An error occurred while fetching the webpage: {url}", exc_info=True
        )
        raise e

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        text_content = soup.get_text(separator=" ", strip=True)
        logging.info(f"Successfully parsed the content of the webpage: {url}")
    except FeatureNotFound as e:
        logging.error(
            "An error occurred while parsing the webpage content.", exc_info=True
        )
        raise e

    return text_content
