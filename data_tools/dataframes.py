import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from data_tools import lookup_parsed_data, load_parsed_data
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter

LIMIT = None


def create_retweet_df(data_dir="../data/14-nov/"):
    return load_parsed_data(data_dir + "parsed_retweets.json", limit=LIMIT,)


def create_tweet_df(recent_offset, crawled_terms, data_dir="../data/14-nov/"):
    cast_cols = {"tweet_count": "int32", "quote_count": "int32"}
    for term in crawled_terms:
        cast_cols[term.lower()] = "Sparse[int8]"
    tweet_df = load_parsed_data(
        data_dir + "parsed_tweets.json",
        exclude_cols={
            "entities",
            "replyTo",
            "replyTo_user",
            "cleaned_text",
            "last_retweeted",
            "place",
            "processed",
            "media",
            "isDeleted",
        },
        limit=LIMIT,
        cast_cols=cast_cols,
    )
    recent_tweet_df = tweet_df[tweet_df.timestamp >= recent_offset]
    old_tweet_df = tweet_df[tweet_df.timestamp < recent_offset]
    del tweet_df

    return old_tweet_df, recent_tweet_df


def create_user_df(data_dir="../data/14-nov/"):
    cast_cols = {
        "followed_cnts": "int32",
        "friends_count": "int32",
        "followers_count": "int32",
    }
    return load_parsed_data(
        data_dir + "parsed_users.json",
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


def group_df_by_hour(df, count_label="count", column="timestamp"):
    grouped_by_hour = (
        pd.to_datetime(df[column])
        .dt.floor("H")
        .value_counts()
        .rename_axis("date")
        .reset_index(name=count_label)
    ).sort_values(by=["date"])
    return grouped_by_hour.set_index("date").fillna(0)


def aggregate_counts_by_hour(recent_tweet_df, retweet_df, crawled_terms):
    aggregated_by_hour = group_df_by_hour(recent_tweet_df, count_label="tweet count")
    retweet_by_hour = group_df_by_hour(retweet_df, count_label="retweet count")
    aggregated_by_hour = aggregated_by_hour.join(retweet_by_hour)
    for term in crawled_terms:
        filtered_by_crawled_term = recent_tweet_df[recent_tweet_df[term] == 1]
        term_grouped_by_hour = group_df_by_hour(
            filtered_by_crawled_term, count_label=term
        )
        aggregated_by_hour = aggregated_by_hour.join(term_grouped_by_hour)
    return aggregated_by_hour.fillna(0)


def create_most_common_hashtags_df(df_tweets, count_label, k=100):
    counted_hashtags = Counter(
        [
            ("#" + hashtag.lower())
            for hashtags in df_tweets["hashtags"]
            for hashtag in hashtags
        ]
    )
    return pd.DataFrame(
        counted_hashtags.most_common(k), columns=["hashtag", count_label]
    ).set_index("hashtag")


def aggregate_most_common_hashtags(df_tweets, crawled_terms, k=100):
    df_most_common_hashtags = create_most_common_hashtags_df(
        df_tweets, count_label="all tweets", k=k
    )
    for term in crawled_terms:
        filtered_by_crawled_term = df_tweets[df_tweets[term] == 1]
        df_most_common_hashtags = df_most_common_hashtags.join(
            create_most_common_hashtags_df(
                filtered_by_crawled_term, count_label=term, k=k
            ),
            how="outer",
        )
    return df_most_common_hashtags.fillna(0).astype(int)


def create_media_df(tweet_df, data_dir):
    tweet_df_with_media = tweet_df[tweet_df["hasMedia"] == True].set_index(
        "datastore_id"
    )
    # Preserve types when joining
    col_types = tweet_df_with_media.select_dtypes(include=["int", "int32"]).dtypes
    media_df = (
        load_parsed_data(data_dir + "/parsed_media.json",)
        .set_index("datastore_id")
        .drop_duplicates(["media_id", "tweet_id"])
    )
    df_media_with_tweets = media_df.join(tweet_df_with_media, on="tweet_id")
    for col, col_type in col_types.iteritems():
        df_media_with_tweets[col] = df_media_with_tweets[col].fillna(0).astype(col_type)

    return df_media_with_tweets
