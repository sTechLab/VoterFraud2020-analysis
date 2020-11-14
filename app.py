import streamlit as st
from interface.exploration_page import get_exploration_page 

PAGES = {
    "Data Exploration": get_exploration_page
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page()
