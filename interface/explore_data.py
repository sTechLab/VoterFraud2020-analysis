import streamlit as st
from collections import defaultdict
import pandas as pd
import numpy as np
from interface.df_utils import load_pickled_df

TOP_N = 20

def get_column_from_selection(selected_cluster, selected_content):
    if selected_cluster == "All":
        if (selected_content == "Top Users"):
            return "retweet_count_metadata"
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

def get_field_description(selected_cluster, selected_content):
    description = "### Field Description"
    if (selected_content == "Top Users"):
        description += ("""
- **retweet_count_metadata**: Aggregated count of retweets that the user received from other users. Limited to tweets that were streamed during the collection of the dataset (Oct 23rd-Dec 16th).
- **retweet_count_streamed**: Aggregated count of retweets that the user received from other users. Limited to tweets and retweets that were streamed during the collection of the dataset (a subset of *retweet_count_metadata*).
- **user_active_status**: Whether the account was active or suspended (as of January 10th).
        """)
    else:
        col = get_column_from_selection(selected_cluster, selected_content)
        if selected_content == "Top Tweets":
            count_text = "the tweet received"
        elif selected_content == "Top Hashtags":
            count_text = "tweets containing the hashtag received"
        elif selected_content == "Top URLs":
            count_text = "tweets containing the URL received"
        elif selected_content == "Top Youtube Videos":
            count_text = "tweets containing a link to the YouTube video received"
        
        if (selected_cluster == "Promoters of Voter Fraud Claims"):
            count_text += " from users in sub-communities 1, 2, 3 and 4"
        elif (selected_cluster == "Detractors of Voter Fraud Claims"):
            count_text += " from users in sub-community 0"
        elif (selected_cluster == "Community 0"):
            count_text += " from users in sub-community 0"
        elif (selected_cluster == "Community 1"):
            count_text += " from users in sub-community 1"
        elif (selected_cluster == "Community 2"):
            count_text += " from users in sub-community 2"
        elif (selected_cluster == "Community 3"):
            count_text += " from users in sub-community 3"
        elif (selected_cluster == "Community 4"):
            count_text += " from users in sub-community 4"
        elif (selected_cluster == "Suspended Users"):
            count_text += " from suspended users"
        
        if (selected_cluster == "All"):
            limitation = "tweets"
        else:
            limitation = "tweets and retweets"

        description += """
- **{}**: Aggregated count of retweets that {}. 
Limited to {} that were streamed during the collection of the dataset (Oct 23rd-Dec 16th).
        """.format(col, count_text, limitation)
    
    description += "\nRead [the paper](https://arxiv.org/abs/2101.08210) and [the Github documentation](https://github.com/sTechLab/Voterfraud2020#data-description) for a detailed explanation of all fields."
    return description


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
            # df_top_users = load_pickled_df("./interface/data/top_users.pickle")
            # df_table = df_top_users.nlargest(10, column)[["handle", column]]
            # df_table.index = [""] * len(df_table)
            # return df_table
            column = "retweet_count_metadata"
            df_top_users = filter_dataframe(
                load_pickled_df("./interface/data/top_users.pickle"),
                selected_cluster,
                selected_content,
            )
            df_table = df_top_users.nlargest(TOP_N, column)[["handle", "followers_count", "user_active_status", "retweet_count_streamed", column]]
            df_table.index = [""] * len(df_table)
            return df_table

        elif selected_content == "Top Tweets":
            df_top_tweets = load_pickled_df("./interface/data/top_tweets.pickle")
            df_table = df_top_tweets.nlargest(TOP_N, column)[["text", column]]
            df_table.index = [""] * len(df_table)
            return df_table

        elif selected_content == "Top Hashtags":
            df_top_hashtags = load_pickled_df("./interface/data/top_hashtags.pickle")
            df_table = df_top_hashtags.nlargest(TOP_N, column)[[column]]
            #df_table.index = [""] * len(df_table)
            return df_table

        elif selected_content == "Top Youtube Videos":
            df_top_videos = load_pickled_df("./interface/data/top_youtube_videos.pickle")
            df_top_videos["video_url"] = df_top_videos.apply(lambda x: "http://youtu.be/" + x.name, axis=1)
            df_top_videos["channel_url"] = df_top_videos.apply(lambda x: "http://youtube.com/channel/" + x["channel_id"], axis=1)
            df_table = df_top_videos.nlargest(TOP_N, column)[["video_url", "channel_title", "channel_url", column]]
            df_table.index = [""] * len(df_table)
            return df_table
        
        elif selected_content == "Top URLs":
            df_top_urls = load_pickled_df("./interface/data/top_urls.pickle")
            df_table = df_top_urls.nlargest(TOP_N, column)[["domain", column]]
            #df_table.index = [""] * len(df_table)
            return df_table

    elif selected_method == "Show content that originated in the selected cluster":
        column = "retweet_count_streamed"

        if selected_content == "Top Users":
            df_top_users = filter_dataframe(
                load_pickled_df("./interface/data/top_users.pickle"),
                selected_cluster,
                selected_content,
            )
            df_table = df_top_users.nlargest(TOP_N, column)[["handle", column]]
            df_table.index = [""] * len(df_table)
            return df_table

        elif selected_content == "Top Tweets":
            df_top_tweets = filter_dataframe(
                load_pickled_df("./interface/data/top_tweets.pickle"),
                selected_cluster,
                selected_content,
            )
            df_table = df_top_tweets.nlargest(TOP_N, column)[["text", column]]
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

    st.markdown(get_field_description(selected_cluster, selected_content))
    st.table(get_content_dataframe(selected_cluster, selected_content, selected_method))


if __name__ == "__main__":
    get_explore_data_page()
