import streamlit as st
from data_tools import load_crawled_terms
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

img_retweet_graph = Image.open("./interface/img/retweet-graph.png")
img_retweet_graph_suspended = Image.open(
    "./interface/img/retweet-graph-suspended-orange.png"
)


def get_landing_page(shared_state):
    coverage_stats = shared_state.coverage_stats

    st.header("VoterFraud2020")
    st.markdown(
        """
        VoterFraud2020 is a multi-modal Twitter dataset with 7.6M tweets and 25.6M retweets related to voter fraud claims.

        ### Download the dataset
        - [Github Repository](https://github.com/sTechLab/VoterFraud2020)
        - [Fighshare](https://doi.org/10.6084/m9.figshare.13571084)

    """.format(
            coverage_stats["recent_tweet_count"] - coverage_stats["quote_tweet_count"],
            coverage_stats["quote_tweet_count"],
            coverage_stats["retweet_count"],
        )
    )
    st.subheader("")
    col1, col2 = st.beta_columns(2)
    col1.image(img_retweet_graph, use_column_width=True)
    col2.image(img_retweet_graph_suspended, use_column_width=True)


if __name__ == "__main__":
    get_landing_page()
