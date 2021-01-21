import streamlit as st
from collections import defaultdict
import pandas as pd
import numpy as np
from .image_urls import bucket_image_urls

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
        Since the graph only includes retweeting and retweeted users, this number corresponds to 73.8% of all users in our dataset.


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

    col1, col2 = st.beta_columns(2)
    col1.markdown("![Table 1]({})".format(bucket_image_urls["community_stats"]))
    col2.markdown("![Figure 1]({})".format(bucket_image_urls["retweet_graph"]))
    st.markdown("""
        _**Table 1 & Figure 1:** Five communities in the retweet graph of people posting about voter-fraud claims; the blue cluster on the left side is mostly of detractors of the claims._
    """)

    st.markdown(
        """
        We visualize the retweet network using the Force Atlast 2 layout in Gephi.
        Figure 1 indicates that the nodes are split between two distinct 
        clusters - community 0 (blue), which mostly consists of _"detractors"_ of the claims, and communities 1, 2, 3 and 4 _("promoters")_ on the right. 
    """
    )

    st.markdown(
        """
        ### Labeling Suspended & Deleted Users
        The VoterFraud2020 dataset is also enhanced with metadata about the users' active status. 
        In total 3.9% of the accounts (99,884) in the data were suspended.
    """
    )
    st.markdown("![Figure 2]({})".format(bucket_image_urls["retweet_graph_suspended"]))
    st.markdown("""
        **Figure 2:** Where suspended users were located in the retweet graph (orange); they mostly came from a specific subcommunity of claim promoters.
    """)


if __name__ == "__main__":
    get_retweet_graph_analysis_page()
