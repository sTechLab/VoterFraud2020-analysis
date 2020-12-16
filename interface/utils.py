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
def group_df_by_hour(df, column="timestamp"):
    grouped_by_hour = (
        pd.to_datetime(df[column])
        .dt.floor("H")
        .value_counts()
        .rename_axis("date")
        .reset_index(name="count")
    ).sort_values(by=["date"])
    return grouped_by_hour.set_index("date")


# @st.cache
def plot_hourly_coverage(df, title):
    df_by_hour = group_df_by_hour(df)
    rolling_average = df_by_hour.rolling("12h").mean()

    fig, ax = plt.subplots()

    ax.plot(
        df_by_hour["count"], label="Hourly", marker=".", linestyle="-", linewidth=0.5
    )
    ax.plot(
        rolling_average["count"],
        marker=".",
        linestyle="-",
        label="12-Hour Rolling Mean",
    )

    ax.legend()

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    # mdates.HourLocator(interval = 12)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

    ax.set_title("Coverage for '{}' (total={:,})".format(title, len(df.index)))

    return fig


@st.cache
def lookup_parsed_tweet_data(indices):
    return lookup_parsed_data("./data/14-nov/parsed_tweets.json", indices)


@st.cache(allow_output_mutation=True, persist=True)
def load_tweet_df(recent_offset, crawled_terms):
    cast_cols = {"tweet_count": "int32", "quote_count": "int32"}
    for term in crawled_terms:
        cast_cols[term.lower()] = "Sparse[int8]"
    tweet_df = load_parsed_data(
        "./data/14-nov/parsed_tweets.json",
        exclude_cols={
            "entities",
            "replyTo",
            "replyTo_user",
            "cleaned_text",
            "text",
            "last_retweeted",
            "place",
            "processed",
            "media",
            "isDeleted"
        },
        verbose=True,
        limit=LIMIT,
        cast_cols=cast_cols,
    )
    recent_tweet_df = tweet_df[tweet_df.timestamp >= recent_offset]
    old_tweet_df = tweet_df[tweet_df.timestamp < recent_offset]
    del tweet_df

    return old_tweet_df, recent_tweet_df


@st.cache(allow_output_mutation=True, persist=True)
def load_retweet_df():
    return load_parsed_data(
        "./data/14-nov/parsed_retweets.json",
        exclude_cols={"tokens", "cleaned_text", "text", "last_retweeted"},
        limit=LIMIT,
    )


@st.cache(allow_output_mutation=True, persist=True)
def load_user_df():
    cast_cols = {
        "followed_cnts": "int32",
        "friends_count": "int32",
        "followers_count": "int32",
    }
    return load_parsed_data(
        "./data/14-nov/parsed_users.json",
        exclude_cols={"description"},
        limit=LIMIT,
        cast_cols=cast_cols,
        index_col="datastore_id",
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


@st.cache(allow_output_mutation=True)
def most_common_hashtags(tweet_df, k=10):
    counted_hashtags = Counter(
        [
            ("#" + hashtag.lower())
            for hashtags in tweet_df["hashtags"]
            for hashtag in hashtags
        ]
    )
    return pd.DataFrame(
        counted_hashtags.most_common(k), columns=["hashtag", "tweet count"]
    )


STOP_WORDS = STOP_WORDS.union({"pron", "", " ", "”", "“", "🇺"})


def include_token(token):
    return token not in STOP_WORDS and not token.startswith("hashtag")


@st.cache(allow_output_mutation=True)
def most_common_tokens(tweet_token_df, k=10):
    counted_tokens = Counter(
        [
            token
            for tokens in tweet_token_df["tokens"]
            for token in tokens
            if include_token(token)
        ]
    )
    return pd.DataFrame(counted_tokens.most_common(k), columns=["token", "tweet count"])
