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


def get_weekly_tweet_analysis_page(shared_state):
    st.header("Top Tweets")
    df_weekly_top_tweets = shared_state.df_weekly_top_tweets
    df_weekly_top_users = shared_state.df_weekly_top_users

    weeks = df_weekly_top_tweets.index.unique(level="WeekDate")
    selected_week_option = st.selectbox(
        "Select a week", get_week_options(weeks), format_func=lambda x: x["label"],
    )
    COLUMNS = [
        "handle",
        "quote_count",
        "retweet_count",
        "timestamp",
        "text"
    ]

    col1, col2 = st.beta_columns(2)
    tweets_top_n = col1.number_input("Show top N tweets", value=5)
    tweets_sort_column = col2.selectbox(
        "Sort by column", ["retweet_count", "quote_count"]
    )
    only_media_tweets = st.checkbox("Only show media tweets")
    df_top_tweets = filter_by_week_option_value(
        df_weekly_top_tweets,
        selected_week_option["value"],
        lambda df: df.set_index("datastore_id"),
    )
    if only_media_tweets:
        df_top_tweets = df_top_tweets[df_top_tweets.hasMedia]
    df_top_tweets = df_top_tweets[COLUMNS].nlargest(tweets_top_n, [tweets_sort_column])
    st.table(df_top_tweets)


if __name__ == "__main__":
    get_weekly_tweet_analysis_page()
