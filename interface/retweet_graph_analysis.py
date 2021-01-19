import streamlit as st
from collections import defaultdict
import pandas as pd
import numpy as np
from PIL import Image

img_retweet_graph = Image.open("./interface/img/retweet-graph.png")
img_community_stats = Image.open("./interface/img/community_stats.png")
img_retweet_graph_suspended = Image.open(
    "./interface/img/retweet-graph-suspended-orange-min.jpg"
)


def get_retweet_graph_analysis_page(shared_state):
    coverage_stats = shared_state.coverage_stats

    st.header("Retweet Graph Analysis")
    st.markdown(
        """
        We constructed a retweet graph of the VoterFraud2020 dataset, where nodes 
        represent users and directed edges correspond to retweets between the users. 
        The direction of an edge corresponds to the direction of the information 
        spreading in the retweet relation. Edges are weighted according to the 
        number of times the corresponding source user has been retweeted. 
        The resulting network consists of 1,887,736 nodes and 16,718,884 edges.


        ### Community Detection using Infomap
        To detect communities within the graph, we used the [Infomap community detection 
        algorithm](https://mapequation.github.io/infomap/python/), which captures the flow of information in directed networks.
        Using the default parameters, the algorithm produces thousands of clusters. 
        By excluding all clusters that contain fewer than 1% of the nodes we are left 
        with 90% of all nodes which are clustered into five communities.


    """.format(
            coverage_stats["recent_tweet_count"] - coverage_stats["quote_tweet_count"],
            coverage_stats["quote_tweet_count"],
            coverage_stats["retweet_count"],
        )
    )

    df_community_stats = pd.DataFrame(
        [
            [0, 860976, 45.6],
            [1, 437783, 23.2],
            [2, 342184, 18.1],
            [3, 33857, 1.8],
            [4, 23414, 1.2],
        ],
        columns=["Community", "Users", "% relative size"],
    )

    # df_community_stats.index = [""] * len(df_community_stats)

    col1, col2 = st.beta_columns(2)
    col1.image(img_community_stats, use_column_width=True)
    # col1.table(df_community_stats.round(1).astype("str"))
    col2.image(img_retweet_graph, use_column_width=True)

    st.markdown(
        """
        We visualize the retweet network using the Force Atlast 2 layout in Gephi.
        The visualization above indicates that the nodes are split between two distinct 
        clusters - community 0 (blue) on the left and communities 1, 2, 3 and 4 on the right. 
    """
    )

    st.markdown(
        """
        The VoterFraud2020 dataset is also enhanced with metadata about the users' suspension status. 
        In total 3.9% of the accounts (99,884) in the data were suspended.

        The visualization below shows that Twitter have primarily suspended users in the "promoters"-cluster
        (suspended users colored in orange):
    """
    )
    st.image(img_retweet_graph_suspended, use_column_width=True)


if __name__ == "__main__":
    get_retweet_graph_analysis_page()
