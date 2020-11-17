import streamlit as st
from data_tools import load_parsed_data, load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from .utils import (
    plot_hourly_coverage,
    load_tweet_df,
    create_crawled_terms_df,
    lookup_parsed_tweet_data,
    load_df,
)
import numpy as np

# Plot styles
import matplotlib.style as style
import json

style.use("seaborn-poster")
style.use("ggplot")

CRAWLED_TERMS = load_crawled_terms("./keywords-3nov.txt")


def get_crawled_terms_page(LIMIT=None):
    st.header("Crawled terms")

    with st.spinner("Loading retweet data"):
        retweet_df = load_df(
            "./data/14-nov/parsed_retweets.json",
            exclude_cols={"tokens", "cleaned_text", "text", "last_retweeted"},
            limit=LIMIT,
        )

    with st.spinner("Loading tweet data"):
        old_tweet_df, recent_tweet_df = load_tweet_df(
            retweet_df.timestamp.min(), CRAWLED_TERMS
        )

    st.subheader("List of Crawled Terms (since 3rd of November)")
    crawled_terms_df = create_crawled_terms_df(CRAWLED_TERMS, recent_tweet_df)
    st.dataframe(crawled_terms_df)

    selected_crawled_term = st.selectbox("Select term", crawled_terms_df["term"].values)

    if selected_crawled_term in recent_tweet_df.columns:
        filtered_by_crawled_term = recent_tweet_df[
            recent_tweet_df[selected_crawled_term] == 1
        ]
        st.pyplot(plot_hourly_coverage(filtered_by_crawled_term, selected_crawled_term))

    term_stats = (
        recent_tweet_df[recent_tweet_df[selected_crawled_term] == 1][
            ["retweet_count", "quote_count"]
        ]
        .fillna(0)
        .astype(int)
    )
    top_retweeted = term_stats.nlargest(10, "retweet_count")
    top_quoted = term_stats.nlargest(10, "quote_count")

    st.subheader("10 most retweeted tweets for '{}'".format(selected_crawled_term))
    st.table(
        pd.DataFrame(
            map(
                lambda t: [t["text"], t["quote_count"], t["retweet_count"]],
                lookup_parsed_tweet_data(top_retweeted.index.values),
            ),
            columns=["text", "quote_count", "retweet_count"],
        )
    )

    st.subheader("10 most quoted tweets for '{}'".format(selected_crawled_term))
    st.table(
        pd.DataFrame(
            map(
                lambda t: [t["text"], t["quote_count"], t["retweet_count"]],
                lookup_parsed_tweet_data(top_quoted.index.values),
            ),
            columns=["text", "quote_count", "retweet_count"],
        )
    )

    st.subheader("Co-occurrence matrix")

    terms_in_df = [term for term in crawled_terms_df["term"]]
    crawled_terms_tweet_df = recent_tweet_df[terms_in_df].sparse.to_dense().astype("int32")
    co_occurrence = crawled_terms_tweet_df.T.dot(crawled_terms_tweet_df)

    st.dataframe(co_occurrence)

    co_occurrence_diagonal = np.diagonal(co_occurrence)

    with np.errstate(divide="ignore", invalid="ignore"):
        co_occurrence_percentage = np.nan_to_num(
            np.true_divide(co_occurrence, co_occurrence_diagonal[:, None])
        )

    st.subheader("Co-occurence matrix (log percentage)")
    st.dataframe(
        pd.DataFrame(
            np.log(co_occurrence_percentage),
            index=co_occurrence.index,
            columns=co_occurrence.columns,
        )
    )


if __name__ == "__main__":
    get_crawled_terms_page()
