""" Module that handles the entry point of the streamlit GUI """
import sys
import os
import warnings
import time
import streamlit as st

from urllib.error import HTTPError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(page_title="KIT Grade Analyzer", layout="wide", page_icon="🎓")

from src.dataloader import DataLoader
from src.guard import Guard

import src.utils as utils
import src.constants as constants
import src.text as text

import gui.visualizations as visualizations


def run_gui() -> None:
    """
    Entry point to the streamlit GUI
    """
    _render_sidebar()
    # Get Input URL
    input_txt: str = st.text_input("Enter one or more URL(s) to PDF to analyze:",
                                   placeholder="https://www.sle.kit.edu/dokumente/ects-tabellen//ECTS_Tab_WS23_24_MA_Informatik_DE.pdf",
                                   max_chars=4096,
                                   help="You can enter one or more URL(s) to the PDF, but if more than one, it "
                                        f"has to be seperated be '{constants.SEP}'. \n\n"
                                        f"For example: <URL1>\{constants.SEP}<URL2>\{constants.SEP}<URL3>")

    if len(input_txt) == 0:
        _render_intro_text()
        return

    url_list: list[str] = utils.separate_input_string(input_txt, sep=constants.SEP)

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
                ["View Bar Plot", "View Normalized Bar Plot", "View Cumulative Distribution (CDF)", "View Raw Data"]
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
        st.error("HTTPError: Please try a different URL.", icon="⚠️")
    except KeyError:
        st.error("KeyError: Please try a different URL. "
                 "Make sure that you are using the newer version of the PDFs", icon="⚠️")


def _render_sidebar() -> None:
    """
    Simply renders and displays the sidebar content.
    """
    with st.sidebar:
        st.image("assets/Logo_KIT.svg-2.png")
        st.write(text.SIDEBAR_CONTENT)


def _render_intro_text() -> None:
    """
    Simply displays the introduction text
    """
    st.markdown(text.INTRO_CONTENT)


run_gui()
