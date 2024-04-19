""" Module that handles the entry point of the streamlit GUI """

import sys
import os
import warnings
import time
import logging
import streamlit as st

from urllib.error import HTTPError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
warnings.simplefilter(action="ignore", category=FutureWarning)
st.set_page_config(page_title="KIT Grade Analyzer", layout="wide", page_icon="🎓")

from src.dataloader import DataLoader
from src.guard import Guard

import src.utils as utils
import src.constants as constants
import src.text as text
import src.scraper as scraper

import gui.visualizations as visualizations

utils.setup_logging(loglevel=constants.LOGLEVEL)
logger = logging.getLogger(__name__)


def run_gui() -> None:
    """
    Entry point to the streamlit GUI
    """
    _render_sidebar()

    # First scrape all currently available studies
    study_dict: dict[str, str] = scraper.scrape_ects_chart(url=constants.URL_TO_CHART)

    # Display Multiselect widget
    selected_studies: dict[str] = st.multiselect(label="Choose your field of study.",
                                                 options=list(study_dict.keys()),
                                                 max_selections=8,
                                                 help="You can select one or more studies to analyze starting from "
                                                      "WS22/23")

    # Match study (key of study_dict) with url (value of study_dict)
    url_list: list[str] = [study_dict[key] for key in selected_studies]

    # Check each input url for validity and safety
    for url in url_list:
        if not Guard(url).check_input():
            st.error("Please try a different URL.", icon="⚠️")
            return

    # Get Data and perform Analysis
    try:
        if st.button("Analyze 🚀", type="primary"):
            with st.spinner("Crawling and processing data ..."):
                df_list = []
                cohort_list = []
                for url in url_list:
                    time.sleep(1)
                    dataloader = DataLoader(url)
                    dataloader.load_data()
                    df = dataloader.get_df()
                    df_list.append(df)
                    cohort_list.append(dataloader.get_study())

            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "View Bar Plot",
                    "View Normalized Bar Plot",
                    "View Cumulative Distribution (CDF)",
                    "View Raw Data",
                ]
            )

            with tab1:
                visualizations.bar_plot_view(df_list, cohort_list)
            with tab2:
                visualizations.bar_plot_normalized_view(df_list, cohort_list)
            with tab3:
                visualizations.cdf_view(df_list, cohort_list)
            with tab4:
                visualizations.raw_data_view(df_list, cohort_list)
    except IndexError:
        st.error("Please try a different URL.", icon="⚠️")
    except HTTPError:
        st.error(
            "HTTPError: Please try a different URL.\nNote that if you add more than one URL, "
            f"they have to be seperated using the '{constants.SEP}' token.",
            icon="⚠️",
        )
    except KeyError:
        st.error(
            "KeyError: Please try a different URL.\n"
            "Make sure that you are using the newer version of the PDFs.",
            icon="⚠️",
        )


def _render_sidebar() -> None:
    """
    Simply renders and displays the sidebar content.
    """
    with st.sidebar:
        st.image("assets/Logo_KIT.svg-2.png")
        st.write(text.SIDEBAR_CONTENT)


run_gui()
