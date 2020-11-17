import streamlit as st
from data_tools import load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from .utils import (
    plot_hourly_coverage,
    load_df,
    load_tweet_df,
)
import numpy as np

# Plot styles
import matplotlib.style as style
import json

style.use("seaborn-poster")
style.use("ggplot")

CRAWLED_TERMS = load_crawled_terms("./keywords-3nov.txt")

def get_basic_stats_page(LIMIT = None):
    st.header("Tweet & Retweet Stats")

    with st.spinner("Loading user data"):
        user_df = load_df(
            "./data/14-nov/parsed_users.json",
            exclude_cols={"description"},
            limit=LIMIT,
        )

    with st.spinner("Loading retweet data"):
        retweet_df = load_df(
            "./data/14-nov/parsed_retweets.json",
            exclude_cols={"tokens", "cleaned_text", "text", "last_retweeted"},
            limit=LIMIT,
        )

    with st.spinner("Loading tweet data"):
        old_tweet_df, recent_tweet_df = load_tweet_df(retweet_df.timestamp.min(), CRAWLED_TERMS)

    st.subheader("Basic stats")
    st.markdown(
        """
        **Number of tweets:** {:,}  
        **Number of tweets after October 23rd:** {:,}  
        **Number of retweets:** {:,}  
        **Number of users:** {:,}

    """.format(
            len(recent_tweet_df.index) + len(old_tweet_df.index),
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
            old_tweet_df.timestamp.min(),
            recent_tweet_df.timestamp.max(),
            retweet_df.timestamp.min(),
            retweet_df.timestamp.max(),
        )
    )

    st.subheader("Hourly Coverage")
    st.pyplot(plot_hourly_coverage(retweet_df, "Retweets"))
    st.pyplot(plot_hourly_coverage(recent_tweet_df, "Tweets since Oct 23rd"))


if __name__ == "__main__":
    get_basic_stats_page()
