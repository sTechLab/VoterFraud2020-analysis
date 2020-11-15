import streamlit as st
from interface.tweet_analysis import get_tweet_analysis_page 

PAGES = {
    "Tweet Analysis": get_tweet_analysis_page
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page()
