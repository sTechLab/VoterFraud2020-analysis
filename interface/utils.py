import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from data_tools import lookup_parsed_data, load_parsed_data
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter

LIMIT = None

@st.cache(allow_output_mutation=True)
def plot_hourly_coverage(df_counts_by_hour, col, title):
    data = df_counts_by_hour[col]
    rolling_average = data.rolling("12h").mean()

    fig, ax = plt.subplots()

    ax.plot(
        data, label="Hourly", marker=".", linestyle="-", linewidth=0.5
    )
    ax.plot(
        rolling_average,
        marker=".",
        linestyle="-",
        label="12-Hour Rolling Mean",
    )

    ax.legend()

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    # mdates.HourLocator(interval = 12)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

    ax.set_title("Coverage for '{}' (total={:,})".format(title, data.sum()))

    return fig


@st.cache
def lookup_parsed_tweet_data(indices):
    return lookup_parsed_data("./data/14-nov/parsed_tweets.json", indices)


def create_crawled_terms_df(crawled_terms, tweet_df):
    crawled_terms_stats = []

    for term in crawled_terms:
        if term in tweet_df.columns:
            stats = {}
            stats["term"] = term
            stats["tweet count"] = tweet_df[term].value_counts().values[1]
            crawled_terms_stats.append(stats)

    crawled_terms_df = pd.DataFrame(crawled_terms_stats).sort_values(
        by=["tweet count"], ascending=False
    )

    return crawled_terms_df


def get_most_common(df_most_common, col, k=10):
    return df_most_common[col].nlargest(k)
