import streamlit as st
from collections import defaultdict
import pandas as pd
import numpy as np
from PIL import Image

img_retweet_graph = Image.open("./interface/img/retweet-graph.png")
img_retweet_graph_suspended = Image.open(
    "./interface/img/retweet-graph-suspended-orange-min.jpg"
)


def get_landing_page(shared_state):
    coverage_stats = shared_state.coverage_stats

    st.header("VoterFraud2020")
    st.markdown(
        """
        We are making publicly available [VoterFraud2020](https://github.com/sTechLab/VoterFraud2020), a multi-modal Twitter 
        dataset with 7.6M tweets and 25.6M retweets that include key phrases 
        and hashtags related to voter fraud claims between October 23rd and December 16th. 

        The dataset also includes the full set of links and YouTube videos shared in these tweets, 
        with data about their spread in different Twitter sub-communities. 

        The methodology for our data collection is detailed in [the paper 
        available from Arxiv](link-to-paper). 
        
        Our hope is that the dataset will be used to study the spread, reach, and 
        dynamics of the voter fraud campaign on Twitter. The data can help expose how different 
        public figures spread different claims, and what kind of engagement various narratives received. 
        

        The paper, dataset, and the initial analysis provided here is a collaboration between the 
        [Social Technologies Lab](https://s.tech.cornell.edu/) at Cornell Tech and Technion. Inquiries should go to Professor Mor Naaman at [mor.naaman@cornell.edu](mailto:mor.naaman@cornell.edu).

        ### Key Takeaways
        - Community detection performed on the dataset reveals that there are 5 sub-communities involved in the discussion. 
        The dataset is enhanced with community labels to enable quick study of how URLs, images and youtube videos spread within these sub-communities.
        - 99,884 suspended users are labeled in the dataset, allowing the investigation of [Twitter's response](https://blog.twitter.com/en_us/topics/company/2021/protecting--the-conversation-following-the-riots-in-washington--.html) to voter fraud claims.
        Preliminary analyses show that Twitter’s ban actions mostly affected a specific community of voter fraud claim promoters.


        *Anton Abilov, Yiqing Hua, Hana Matatov, Ofra Amir & Mor Naaman.*

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
