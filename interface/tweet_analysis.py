import streamlit as st
from data_tools import load_parsed_data, load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from .utils import plot_hourly_coverage
import numpy as np

# Plot styles
import matplotlib.style as style
import json

style.use("seaborn-poster")
style.use("ggplot")

LIMIT = None

CRAWLED_TERMS = load_crawled_terms("./keywords-3nov.txt")


@st.cache(allow_output_mutation=True, persist=True)
def load_tweet_df():
    cast_cols = {"tweet_count": "int32", "quote_count": "int32"}
    for term in CRAWLED_TERMS:
        cast_cols[term] = "Sparse[int8]"
    return load_parsed_data(
        "./data/14-nov/parsed_tweets.json",
        exclude_cols={
            "tokens",
            "cleaned_text",
            "text",
            "last_retweeted",
            "place",
            "processed",
            "media",
            "isDeleted",
        },
        verbose=True,
        limit=LIMIT,
        cast_cols=cast_cols,
    )


@st.cache(allow_output_mutation=True, persist=True)
def load_df(filename, include_cols=None, exclude_cols={}, limit=None):
    return load_parsed_data(
        filename,
        include_cols=include_cols,
        exclude_cols=exclude_cols,
        verbose=True,
        limit=limit,
    )


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


def lookup_parsed_tweet_data(indices):
    counter = 0
    data = []
    with open("./data/14-nov/parsed_tweets.json") as r:
        for line in r:
            if counter in indices:
                data.append(json.loads(line))
                if len(data) == len(indices):
                    break
            counter += 1
    return data


def get_tweet_analysis_page():
    st.header("Tweet Analysis")

    with st.spinner("Loading user data"):
        user_df = load_df(
            "./data/14-nov/parsed_users.json",
            exclude_cols={"description"},
            limit=LIMIT,
        )

    with st.spinner("Loading tweet data"):
        tweet_df = load_tweet_df()

    with st.spinner("Loading retweet data"):
        retweet_df = load_df(
            "./data/14-nov/parsed_retweets.json",
            exclude_cols={"tokens", "cleaned_text", "text", "last_retweeted"},
            limit=LIMIT,
        )

    recent_tweet_df = tweet_df[tweet_df.timestamp > retweet_df.timestamp.min()]

    crawled_terms = CRAWLED_TERMS

    st.subheader("Basic stats")
    st.markdown(
        """
        **Number of tweets:** {}  
        **Number of tweets after October 23rd:** {}  
        **Number of retweets:** {}  
        **Number of users:** {}

    """.format(
            len(tweet_df.index),
            len(recent_tweet_df.index),
            len(retweet_df.index),
            len(user_df.index),
        )
    )

    st.subheader("Coverage")
    st.markdown(
        """
        **Earliest tweet:** {}  
        **Latest tweet:** {}  
        **Earliest retweet:** {}  
        **Latest retweet:** {}  

    """.format(
            tweet_df.timestamp.min(),
            tweet_df.timestamp.max(),
            retweet_df.timestamp.min(),
            retweet_df.timestamp.max(),
        )
    )

    st.subheader("Hourly Coverage")
    st.pyplot(plot_hourly_coverage(retweet_df, "Retweets"))
    st.pyplot(plot_hourly_coverage(recent_tweet_df, "Tweets since Oct 23rd"))

    st.subheader("Crawled terms (since 3rd of November)")

    crawled_terms_df = create_crawled_terms_df(crawled_terms, recent_tweet_df)
    st.dataframe(crawled_terms_df)

    selected_crawled_term = st.selectbox("Select term", crawled_terms_df["term"].values)

    if selected_crawled_term in recent_tweet_df.columns:
        filtered_by_crawled_term = recent_tweet_df[
            recent_tweet_df[selected_crawled_term] == 1
        ]
        st.pyplot(plot_hourly_coverage(filtered_by_crawled_term, selected_crawled_term))

    term_stats = (
        tweet_df[tweet_df[selected_crawled_term] == 1][["retweet_count", "quote_count"]]
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

    terms_in_df = [term for term in crawled_terms if term in tweet_df.columns]
    crawled_terms_tweet_df = tweet_df[terms_in_df].sparse.to_dense().astype("int32")
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
    get_tweet_analysis_page()
