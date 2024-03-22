import sys
import os
import warnings
import time

import streamlit as st
import plotly.express as px
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(layout="wide")

from src.dataloader import DataLoader
from src.guard import Guard


def run_gui() -> None:
    _render_sidebar()
    # Get Input URL
    url: str = st.text_input("Enter URL to PDF to analyze:", placeholder="URL to the cohort PDF ...")

    if len(url) == 0:
        st.info("Please enter the URL to the PDF document that you'd like to analyze.\n\n" +
                "You can find the " +
                "ECTS Ranking Charts here: \n\n  https://www.sle.kit.edu/nachstudium/ects-einstufungstabellen.php",
                icon="ℹ️")
        return

    # Check input for validity and safety
    if not Guard(url).check_input():
        st.error("Please try a different URL.", icon="⚠️")
        return

    # Get Data and perform Analysis
    try:
        if st.button("Analyze 🚀", type="primary"):
            with st.spinner("Crawling and Preprocessing Data ..."):
                time.sleep(1)
                dataloader = DataLoader(url)
                dataloader.load_data()
                df = dataloader.get_df()

            tab1, tab2, tab3 = st.tabs(
                ["View Bar Plot", "View Cumulative Distribution (CDF)", "View Raw Data"]
            )

            with tab1:
                _bar_plot_view(df, dataloader)
            with tab2:
                _cdf_view(df, dataloader)
            with tab3:
                _raw_data_view(df)
    except IndexError:
        st.error("Please try a different URL.", icon="⚠️")


def _bar_plot_view(df, dataloader) -> None:
    # View Stats
    _display_stats(df, dataloader)

    # Display Bar Plot
    p = px.bar(df, x="Note", y="Anzahl", title=f"Grade Distribution of Cohort '{dataloader.get_study()}'")
    p.update_xaxes(tickvals=[i/10 for i in range(10, 41)], ticktext=[str(i/10) for i in range(10, 41)])
    p.add_vline(x=np.round(np.average(df['Note'], weights=df['Anzahl']), 4),
                annotation_text="Mean", line_dash="dot", line_color="red")
    st.plotly_chart(p, use_container_width=True)


def _cdf_view(df, dataloader) -> None:
    # View Stats
    _display_stats(df, dataloader)

    # Display CDF
    fig = px.line(df, x="Note", y="Kumuliert", title=f"CDF of Cohort '{dataloader.get_study()}'")
    fig.update_xaxes(tickvals=[i / 10 for i in range(10, 41)], ticktext=[str(i / 10) for i in range(10, 41)])
    fig.add_hline(y=10, annotation_text="Top 10%", line_dash="dot", line_color="red")
    fig.add_hline(y=50, annotation_text="Median", line_dash="dot", line_color="red")
    st.plotly_chart(fig, use_container_width=True)


def _raw_data_view(df) -> None:
    st.dataframe(df)


def _display_stats(df, dataloader) -> None:

    st.metric(label="Cohort", value=dataloader.get_study())
    col1, col2, col3 = st.columns(3)
    # Display Stats
    mean = np.average(df['Note'], weights=df['Anzahl'])
    variance = np.average((df['Note'] - mean) ** 2, weights=df['Anzahl'])
    std = np.sqrt(variance)

    col1.metric(label="Number of Graduates", value=sum(df["Anzahl"]))
    col2.metric(label="Mean", value=np.round(mean, 2))
    col3.metric(label="Standard Deviation", value=np.round(std, 2))


def _render_sidebar() -> None:
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

            ___
            *Made by Alessio Negrini*  
            *Version 0.1, March 2024*
        """)


run_gui()
