import streamlit as st
from collections import defaultdict
import pandas as pd
import numpy as np

CLUSTER_PROMOTERS = "Promoters of Voter Fraud Claims"
CLUSTER_DETRACTORS = "Detractors of Voter Fraud Claims"
CLUSTER_SUSPENDED = "Suspended Users"

def get_top_image_analysis_page(shared_state):
    st.header("Top Images")
    st.markdown(
        """
        We investigated the popularity of images within the promoter and detractor clusters. Popularity is defined by the highest number of retweets by users from each cluster. 
        
        After grouping images by the same [pHash value](https://github.com/sTechLab/VoterFraud2020#images) (a perceptual hash value), we present the top 10 images that have been retweeted in each cluster.
        We also include the total number of tweets in the dataset that shared the image, and the total number of retweets as they appear in metadata.
        
        We present the same analysis for users from the suspended set, i.e. the most retweeted images by users that were suspended from Twitter.

    """
    )

    selected_cluster = st.selectbox(
        "Select cluster",
        [
            CLUSTER_PROMOTERS,
            CLUSTER_DETRACTORS,
            CLUSTER_SUSPENDED,
        ],
    )

    if (selected_cluster == CLUSTER_PROMOTERS):
        selected_df = shared_state.df_images_promoters
    elif (selected_cluster == CLUSTER_DETRACTORS):
        selected_df = shared_state.df_images_detractors
    else:
        selected_df = shared_state.df_images_suspended
    
    for i, tweet_count, cluster_retweet_count, total_retweet_count, image_url in selected_df.itertuples():

        rank = i + 1
        st.markdown(
            """
            ### {}) {:,} retweets from {}
            - Appeared in {} tweets.  
            - Total retweet count: {:,}.  

            ![Image {}]({})
        """.format(rank, cluster_retweet_count, selected_cluster, tweet_count, total_retweet_count, rank, image_url)
        )

if __name__ == "__main__":
    get_top_image_analysis_page()
