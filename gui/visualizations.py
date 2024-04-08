""" Module that handles the visualization / plotly plots"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

import src.constants as constants


def bar_plot_view(df_list: list[pd.DataFrame], cohort_list: list[str]) -> None:
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


def bar_plot_normalized_view(df_list: list[pd.DataFrame], cohort_list: list[str]) -> None:
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


def cdf_view(df_list: list[pd.DataFrame], cohort_list: list[str]) -> None:
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


def raw_data_view(df_list: list[pd.DataFrame], cohort_list: list[str]) -> None:
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
