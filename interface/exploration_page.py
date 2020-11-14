import streamlit as st
from scripts import load_dataflow_export

def get_exploration_page():
    st.header("Data Exploration")
    load_dataflow_export()

if __name__ == "__main__":
    get_exploration_page()