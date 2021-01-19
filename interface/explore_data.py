import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict
import pandas as pd
import numpy as np
from PIL import Image

# Plot styles
import matplotlib.style as style
import json

style.use("seaborn-poster")
style.use("ggplot")

def get_column_from_selection(selected_cluster, selected_content):
    if selected_cluster == "All":
        if (selected_content == "Top Users"):
            return "retweet_count_streamed"
        else:
            return "retweet_count_metadata"
    elif selected_cluster == "Detractors of Voter Fraud Claims":
        return "retweet_count_by_detractors"
    elif selected_cluster == "Promoters of Voter Fraud Claims":
        return "retweet_count_by_promoters"
    elif selected_cluster.startswith("Community"):
        return "retweet_count_by_community_" + selected_cluster.replace(
            "Community ", ""
        )
    elif selected_cluster == "Suspended Users":
        return "retweet_count_by_suspended_users"


def filter_dataframe(df, selected_cluster, selected_content):
    if selected_cluster == "All":
        return df
    elif selected_cluster == "Detractors of Voter Fraud Claims":
        return df[df.user_community == 0]
    elif selected_cluster == "Promoters of Voter Fraud Claims":
        return df[df.user_community != 0]
    elif selected_cluster.startswith("Community"):
        community = int(selected_cluster.replace("Community ", ""))
        return df[df.user_community == community]
    elif selected_cluster.startswith("Suspended Users"):
        return df[df.user_active_status == "suspended"]


def get_content_dataframe(selected_cluster, selected_content, selected_method):
    if selected_method == "Show content by popularity in the selected cluster":
        column = get_column_from_selection(selected_cluster, selected_content)

        if selected_content == "Top Users":
            # df_top_users = pd.read_pickle("./interface/data/top_users.pickle")
            # df_table = df_top_users.nlargest(10, column)[["handle", column]]
            # df_table.index = [""] * len(df_table)
            # return df_table
            column = "retweet_count_streamed"
            df_top_users = filter_dataframe(
                pd.read_pickle("./interface/data/top_users.pickle"),
                selected_cluster,
                selected_content,
            )
            df_table = df_top_users.nlargest(10, column)[["handle", "followers_count", column]]
            df_table.index = [""] * len(df_table)
            return df_table

        elif selected_content == "Top Tweets":
            df_top_tweets = pd.read_pickle("./interface/data/top_tweets.pickle")
            df_table = df_top_tweets.nlargest(10, column)[["text", column]]
            df_table.index = [""] * len(df_table)
            return df_table

        elif selected_content == "Top Hashtags":
            df_top_hashtags = pd.read_pickle("./interface/data/top_hashtags.pickle")
            df_table = df_top_hashtags.nlargest(10, column)[[column]]
            #df_table.index = [""] * len(df_table)
            return df_table

        elif selected_content == "Top Youtube Videos":
            df_top_videos = pd.read_pickle("./interface/data/top_youtube_videos.pickle")
            df_top_videos["video_url"] = df_top_videos.apply(lambda x: "http://youtu.be/" + x.name, axis=1)
            df_table = df_top_videos.nlargest(10, column)[["video_url", "channel_title", column]]
            df_table.index = [""] * len(df_table)
            return df_table
        
        elif selected_content == "Top URLs":
            df_top_urls = pd.read_pickle("./interface/data/top_urls.pickle")
            df_table = df_top_urls.nlargest(10, column)[["domain", column]]
            #df_table.index = [""] * len(df_table)
            return df_table

    elif selected_method == "Show content that originated in the selected cluster":
        column = "retweet_count_streamed"

        if selected_content == "Top Users":
            df_top_users = filter_dataframe(
                pd.read_pickle("./interface/data/top_users.pickle"),
                selected_cluster,
                selected_content,
            )
            df_table = df_top_users.nlargest(10, column)[["handle", column]]
            df_table.index = [""] * len(df_table)
            return df_table

        elif selected_content == "Top Tweets":
            df_top_tweets = filter_dataframe(
                pd.read_pickle("./interface/data/top_tweets.pickle"),
                selected_cluster,
                selected_content,
            )
            df_table = df_top_tweets.nlargest(10, column)[["text", column]]
            df_table.index = [""] * len(df_table)
            return df_table

    return pd.DataFrame()

def get_explore_data_page(shared_state):
    coverage_stats = shared_state.coverage_stats

    st.header("Explore The Dataset")
    col1, col2 = st.beta_columns(2)
    selected_cluster = col1.selectbox(
        "Filter Users",
        [
            "All",
            "Promoters of Voter Fraud Claims",
            "Detractors of Voter Fraud Claims",
            "Suspended Users",
            "Community 0",
            "Community 1",
            "Community 2",
            "Community 3",
            "Community 4",
        ],
    )
    selected_content = col2.selectbox(
        "Select content",
        [
            "Top Users",
            "Top Tweets",
            "Top Hashtags",
            "Top Youtube Videos",
            #"Top Channels",
            "Top URLs",
            #"Top Domains",
        ],
    )

    # selected_method = st.selectbox(
    #     "Method",
    #     [
    #         "Show content that originated in the selected cluster",
    #         "Show content by popularity in the selected cluster",
    #     ],
    # )
    selected_method = "Show content by popularity in the selected cluster"

    st.table(get_content_dataframe(selected_cluster, selected_content, selected_method))


if __name__ == "__main__":
    get_explore_data_page()
