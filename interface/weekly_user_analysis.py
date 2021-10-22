import streamlit as st
from data_tools import load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict
import pandas as pd
import numpy as np
from interface.weekly_utils import (
    filter_by_week_option_value,
    get_week_label,
    get_week_options,
)

# Plot styles
import matplotlib.style as style
import json

style.use("seaborn-poster")
style.use("ggplot")


def get_week_label(week_start):
    week_end = week_start + pd.DateOffset(days=6)
    return "{}-{}".format(week_start.strftime("%m/%d"), week_end.strftime("%m/%d"))


def get_weekly_user_analysis_page(shared_state):
    st.header("Top Users")
    df_weekly_top_tweets = shared_state.df_weekly_top_tweets
    df_weekly_top_users = shared_state.df_weekly_top_users

    weeks = df_weekly_top_tweets.index.unique(level="WeekDate")
    selected_week_option = st.selectbox(
        "Select a week", get_week_options(weeks), format_func=lambda x: x["label"],
    )

    COLUMNS = [
        "handle",
        "name",
        "retweeted_count",
        "quoted_count",
        "all_tweet_count",
        "media_tweet_count",
        "followers_count",
        "verified",
    ]
    col1, col2 = st.columns(2)
    top_n = max(col1.number_input("Show top N users (limited to 25)", value=5), 25)
    sort_column = col2.selectbox(
        "Sort by column",
        [
            "retweeted_count",
            "quoted_count",
            "all_tweet_count",
            "media_tweet_count",
            "followers_count",
        ],
    )
    df_top_users = filter_by_week_option_value(
        df_weekly_top_users,
        selected_week_option["value"],
        lambda df: df
        .reset_index(level="user")
        .groupby(["user", "handle", "name", "followers_count", "verified"])
        .sum()
        .reset_index()
        .set_index("user")
        ,
    )[COLUMNS].nlargest(top_n, [sort_column])
    st.table(df_top_users)


if __name__ == "__main__":
    get_weekly_user_analysis_page()
