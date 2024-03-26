import sys
import os
import warnings
import time

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from urllib.error import HTTPError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(layout="wide")

from src.dataloader import DataLoader
from src.guard import Guard

import src.utils as utils
import src.constants as constants


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
        _view_intro_text()
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
                _bar_plot_view(df_list, cohort_list)
            with tab2:
                _bar_plot_normalized_view(df_list, cohort_list)
            with tab3:
                _cdf_view(df_list, cohort_list)
            with tab4:
                _raw_data_view(df_list, cohort_list)
    except IndexError:
        st.error("Please try a different URL.", icon="⚠️")
    except HTTPError:
        st.error("HTTPError: Please try a different URL.", icon="⚠️")
    except KeyError:
        st.error("KeyError: Please try a different URL. "
                 "Make sure that you are using the newer version of the PDFs", icon="⚠️")


def _bar_plot_view(df_list: list[pd.DataFrame], cohort_list: list[str]) -> None:
    """
    Renders the Bar Plot View.
    :param df_list: list[pd.DataFrame] -- List of parsed pandas DataFrames
    :param cohort_list: list[str] -- List of the cohort names
    :return: None
    """
    # Bar Plot Settings
    fig = go.Figure()
    for df, cohort in zip(df_list, cohort_list):
        fig.add_trace(go.Bar(x=df["Note"], y=df["Anzahl"], name=cohort))
    fig.update_xaxes(tickvals=[i / 10 for i in range(10, 41)], ticktext=[str(i / 10) for i in range(10, 41)])
    fig.update_layout(title='Grade Distribution', xaxis_title='Grade', yaxis_title='Count')
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

    # View Stats
    _display_stats(df_list, cohort_list)


def _bar_plot_normalized_view(df_list: list[pd.DataFrame], cohort_list: list[str]) -> None:
    """
    Renders the Normalized Bar Plot View.
    :param df_list: list[pd.DataFrame] -- List of parsed pandas DataFrames
    :param cohort_list: list[str] -- List of the cohort names
    :return: None
    """
    fig = go.Figure()
    for df, cohort in zip(df_list, cohort_list):
        fig.add_trace(go.Bar(x=df["Note"], y=df["Prozent"], name=cohort))
    fig.update_xaxes(tickvals=[i / 10 for i in range(10, 41)], ticktext=[str(i / 10) for i in range(10, 41)])
    fig.update_layout(title='Normalized Grade Distribution', xaxis_title='Grade', yaxis_title='Percent [%]')
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

    # View Stats
    _display_stats(df_list, cohort_list)


def _cdf_view(df_list: list[pd.DataFrame], cohort_list: list[str]) -> None:
    """
    Renders the Cumulative Distribution Function (CDF) View
    :param df_list: list[pd.DataFrame] -- List of parsed pandas DataFrames
    :param cohort_list: list[str] -- List of the cohort names
    :return: None
    """
    fig = go.Figure()
    for df, cohort in zip(df_list, cohort_list):
        fig.add_trace(go.Line(x=df["Note"], y=df["Kumuliert"], name=cohort))
    fig.update_xaxes(tickvals=[i / 10 for i in range(10, 41)], ticktext=[str(i / 10) for i in range(10, 41)])
    fig.update_layout(title='Cumulative Distribution Function (CDF)', xaxis_title='Grade', yaxis_title='Cumulative [%]')
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.add_hline(y=10, annotation_text="Top 10%", line_dash="dot", line_color="red")
    fig.add_hline(y=50, annotation_text="Median", line_dash="dot", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

    # View Stats
    _display_stats(df_list, cohort_list)


def _raw_data_view(df_list: list[pd.DataFrame], cohort_list: list[str]) -> None:
    """
    Displays the raw data (i.e. the DataFrame)
    :param df_list: list[pd.DataFrame] -- List of parsed pandas DataFrames
    :param cohort_list: list[str] -- List of the cohort names
    :return: None
    """
    col1, col2 = st.columns(2)

    for i, (df, cohort) in enumerate(zip(df_list, cohort_list)):
        if i % 2 == 0:
            col1.subheader(body=f"{cohort}", divider=constants.COL_DIVIDER)
            col1.dataframe(df)
        else:
            col2.subheader(body=f"{cohort}", divider=constants.COL_DIVIDER)
            col2.dataframe(df)



def _display_stats(df_list: list[pd.DataFrame], cohort_list: list[str]) -> None:
    """
    Computes and displays descriptive statistics about the dataframe(s)
    :param df_list: list[pd.DataFrame] -- List of parsed pandas DataFrames
    :param cohort_list: list[str] -- List of the cohort names
    :return: None
    """
    for df, cohort in zip(df_list, cohort_list):
        st.subheader(body=f"{cohort}", divider=constants.COL_DIVIDER)
        col1, col2, col3 = st.columns(3)

        # Compute Stats
        mean = np.average(df['Note'], weights=df['Anzahl'])
        variance = np.average((df['Note'] - mean) ** 2, weights=df['Anzahl'])
        std = np.sqrt(variance)

        # Display Stats
        col1.metric(label="Number of Graduates", value=sum(df["Anzahl"]))
        col2.metric(label="Mean", value=np.round(mean, 2))
        col3.metric(label="Standard Deviation", value=np.round(std, 2))


def _render_sidebar() -> None:
    """
    Simply renders and displays the sidebar content.
    """
    with st.sidebar:
        st.image("assets/Logo_KIT.svg-2.png")
        st.write("""
            # Unofficial KIT Grade Analyzer

            - Simply put the URL to the PDF in the corresponding field and click on the button.
            - You can find the ECTS Ranking Chart here: 
            `https://www.sle.kit.edu/nachstudium/ects-einstufungstabellen.php`
            - Only works with the german version and with the newer version of the documents (i.e. the ones
            with the cumulative column)
            - Example URL would be 
            `https://www.sle.kit.edu/dokumente/ects-tabellen//ECTS_Tab_WS23_24_MA_Informatik_DE.pdf`  
            - To compare two or more cohorts, simply add them into the text field separated by '$'

            ___
            *Made by Alessio Negrini*  
            *Contact: Alessio(d0t|]Negrini[at)live.de*
            *Version 0.1, March 2024*
        """)


def _view_intro_text() -> None:
    """
    Simply displays the introduction text
    """
    st.markdown(f"""
            ## 👋 Hi and welcome to the Unofficial KIT Grade Analyzer  
            **How To Use**  
            - Please enter one or more URL to the PDF document that you'd like to analyze
            - If you are using multiple URLs, please separate them using Seperator Token '\$', e.g. `<URL1>$<URL2>`
            - You can find the ECTS Ranking Chart here: `https://www.sle.kit.edu/nachstudium/ects-einstufungstabellen.php`  
                - Simply click on your cohort and copy the URL to your pdf
                - Note that this Data App only works with never versions of the Ranking (i.e. the ones with the cumulative column)
            """)


run_gui()
