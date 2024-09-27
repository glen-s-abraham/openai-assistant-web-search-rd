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


def fetch_webpage_content(url: str) -> Optional[str]:
    """
    Fetch and parse content from a specified webpage URL.

    Parameters
    ----------
    url : str
        The URL of the webpage to be fetched and parsed.

    Returns
    -------
    Optional[str]
        The textual content of the webpage, or None if fetching fails.

    Raises
    ------
    ValueError
        If the URL is empty.
    """
    if not url:
        raise ValueError("The URL must be a non-empty string.")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        logging.info(f"Successfully fetched the webpage: {url}")
    except (requests.RequestException, ValueError) as e:
        logging.error(f"An error occurred while fetching the webpage: {url}: {e}")
        return None

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        text_content = soup.get_text(separator=" ", strip=True)
        logging.info(f"Successfully parsed the content of the webpage: {url}")
    except Exception as e:
        logging.error(
            f"An error occurred while parsing the webpage content from: {url}: {e}"
        )
        return None

    return text_content


def fetch_and_combine_contents(urls: List[str]) -> Optional[str]:
    """
    Fetch contents of multiple webpages given their URLs and combine the successful results.

    Parameters
    ----------
    urls : List[str]
        The list of webpage URLs to be fetched and combined.

    Returns
    -------
    Optional[str]
        The combined content of successful webpage fetches, or None if no content could be fetched.
    """
    combined_content = []

    for url in urls:
        content = fetch_webpage_content(url)
        if content:
            combined_content.append(f"\n{'*'*25}Content from: {url}{'*'*25}\n{content}\n")
        else:
            logging.info(f"No content fetched from URL: {url}")

    if not combined_content:
        logging.warning("No content could be fetched from the provided URLs.")
        return None

    return " ".join(combined_content)
