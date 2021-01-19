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


def get_top_image_analysis_page(shared_state):
    coverage_stats = shared_state.coverage_stats

    st.header("Top Images")
    st.markdown(
        """
        We investigated the popularity of images within the promoter and detractor clusters. Popularity is defined by the highest number of retweets by users from each cluster. 
        
        After grouping images by the same pHash value (a perceptual hash value), we present the top 10 images that have been retweeted in each cluster.
        We also include the total number of tweets in the dataset that shared the image, and the total number of retweets as they appear in metadata.

    """.format(
            coverage_stats["recent_tweet_count"] - coverage_stats["quote_tweet_count"],
            coverage_stats["quote_tweet_count"],
            coverage_stats["retweet_count"],
        )
    )

    selected_cluster = st.selectbox(
        "Select cluster",
        ["Promoters of Voter Fraud Claims", "Detractors of Voter Fraud Claims", "Suspended Users"],
    )

    
    st.markdown("""
        <style>
        img {
            max-width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        ### 1) 4,700 retweets from detractors of voter fraud claims
        - Appeared in 20 tweets.  
        - Total retweet count: 10,743.  

        ![Image 1](https://storage.googleapis.com/vote-twitter-stream/5547006013472768.jpg)
    """)

    st.markdown("""
        ### 2) 3,424 retweets from detractors of voter fraud claims
        - Appeared in 8 tweets.  
        - Total retweet count: 6,425.  

        ![Image 2](https://storage.googleapis.com/vote-twitter-stream/4674182692470784.jpg)
    """)


if __name__ == "__main__":
    get_top_image_analysis_page()
