import streamlit as st
from interface.tweet_analysis import get_tweet_analysis_page 
from interface.crawled_terms import get_crawled_terms_page 
from interface.basic_stats import get_basic_stats_page

PAGES = {
    "Tweet Analysis": get_tweet_analysis_page,
    #"Tweet & Retweet Stats": get_basic_stats_page,
    #"Crawled Terms": get_crawled_terms_page,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page()
