""" Module that handles the scraping from the ECTS Ranking Table """

import logging
import requests
import streamlit as st

import src.constants as constants

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
_EXCLUDE_SEMESTERS = ["SS22_", "WS21_", "SS21_", "WS20_", "SS20_", "WS19_", "SS19_", "WS18_", "SS18_",
                      "WS17_", "SS17_", "WS16_", "SS16_", "WS15_", "SS15_", "WS14_", "SS14_", "WS13_", "SS13_"]


@st.cache_data
def scrape_ects_chart(url: str = constants.URL_TO_CHART) -> dict[str, str]:
    """
    Scrapes the list of all available cohorts (starting WS23/24) and returns them in a dictionary.
    Dictionary contains the user-friendly title as the key, and the URL to the pdf as value.

    :param url: str -- URL to the ECTS Ranking Tables
    :return: result_dict: dict[str, str] -- Dict with cohort title as key and URL to pdf as value
    """
    # Send a GET request to the URL
    logger.info(f"Scraping title of cohorts: Sending GET request to {constants.URL_TO_CHART} ...")
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all nodes with both title and href attributes
    nodes_with_title_href = soup.find_all(lambda tag: tag.has_attr('title') and tag.has_attr('href'))

    # Empty dict to populate with title as key and link to document as value
    result_dict: dict[str, str] = {}

    # Extract and print the titles and hrefs of these nodes
    for node in nodes_with_title_href:
        title = node['title']
        href = node['href']
        # Filter out any other title elements that do not start with 'ECTS'
        if title.startswith("ECTS"):
            title = title.split("ECTS_Tab_")[1].split(".pdf")[0]
            # Cohorts before WS22/23 are uniquely prefixed, that's why we omit them if they are in the provided list
            semester = title[:5]
            if semester not in _EXCLUDE_SEMESTERS:
                href = constants.HOST + href
                result_dict[title] = href

    return result_dict
