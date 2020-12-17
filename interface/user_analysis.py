import streamlit as st
from data_tools import load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter
import pandas as pd
import numpy as np

# Plot styles
import matplotlib.style as style
import json

style.use("seaborn-poster")
style.use("ggplot")

LIMIT = None


@st.cache(allow_output_mutation=True)
def top_users_by_followers(user_df, k=10, only_verified=None):
    if only_verified:
        user_df = user_df[user_df["verified"] == only_verified]
    return user_df.nlargest(k, "followers_count").sort_values(
        "followers_count", ascending=False
    )[["name", "followers_count"]]


@st.cache(allow_output_mutation=True)
def top_users_by_counts(
    user_df, user_counts, k=10, only_verified=None, count_label="count"
):
    top_users = []
    for user_id, count in user_counts.most_common():
        if user_id not in user_df.index:
            print("User not found " + user_id)
        elif not only_verified or user_df.at[user_id, "verified"]:
            top_users.append(
                {
                    "user_id": user_id,
                    count_label: count,
                    "handle": user_df.at[user_id, "handle"],
                    "name": user_df.at[user_id, "name"],
                }
            )
            if len(top_users) == k:
                break
    return pd.DataFrame(top_users).set_index("user_id")


@st.cache(allow_output_mutation=True)
def get_counts(df, key):
    return Counter(df[key])


DATAFRAME_DIR = "./data/dataframes/14-nov/"


def get_user_analysis_page(shared_state):
    st.header("User Analysis")

    if shared_state.selected_date != "14-dec":
        st.write("Currently disabled for this date range (work in progress)")
        return

    with st.spinner("Loading retweet data"):
        retweet_df = pd.read_pickle(DATAFRAME_DIR + "df_retweets.pickle")

    with st.spinner("Loading tweet data"):
        recent_tweet_df = pd.read_pickle(DATAFRAME_DIR + "df_recent_tweets.pickle")

    user_df = shared_state.user_df

    st.header("Prominent users among all tweets")
    only_verified_users = st.checkbox("Only count verified users", value=True)

    st.subheader("By follower count")
    st.dataframe(top_users_by_followers(user_df, 10, only_verified=only_verified_users))

    st.subheader("By retweet count (number of times they were retweeted)")
    st.dataframe(
        top_users_by_counts(
            user_df,
            get_counts(retweet_df, "retweetedFrom_user"),
            count_label="retweeted count",
            only_verified=only_verified_users,
        )
    )

    st.subheader("By tweet count")
    st.dataframe(
        top_users_by_counts(
            user_df,
            get_counts(recent_tweet_df, "user"),
            count_label="tweet count",
            only_verified=only_verified_users,
        )
    )


if __name__ == "__main__":
    get_user_analysis_page()
