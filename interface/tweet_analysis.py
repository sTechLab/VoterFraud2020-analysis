import streamlit as st
from data_tools import load_parsed_data

def get_tweet_analysis_page():
    st.header("Tweet Analysis")

    df = load_parsed_data('./data/test-2.json')
    
    st.markdown("""
        **Dataframe shape:** {}
    """.format(df.shape))

    st.dataframe(df[:10])
    

if __name__ == "__main__":
    get_tweet_analysis_page()