import streamlit as st
import pandas as pd
from interface.tweet_analysis import get_tweet_analysis_page
from interface.crawled_term_analysis import get_crawled_term_analysis_page
from interface.weekly_user_analysis import get_weekly_user_analysis_page
from interface.url_analysis import get_url_analysis_page
from interface.weekly_tweet_analysis import get_weekly_tweet_analysis_page
import pickle

PAGES = {
    "Overview": get_tweet_analysis_page,
    "Top Tweets": get_weekly_tweet_analysis_page,
    "Top Users": get_weekly_user_analysis_page,
    "URL Analysis": get_url_analysis_page,
    "Filter by crawled term": get_crawled_term_analysis_page,
}

LIMIT = None


class SharedState:
    pass


selected_date = st.selectbox("Select dataset", ["14-nov", "16-dec"], index=1)
DATAFRAME_DIR = "./data/dataframes/{}/".format(selected_date)


@st.cache(allow_output_mutation=True)
def prepare_shared_state():
    print("Preparing Shared State")
    state = SharedState()

    with st.spinner("Loading user data"):
        state.user_df = pd.read_pickle(DATAFRAME_DIR + "df_users.pickle")

    state.crawled_terms_df = pd.read_pickle(DATAFRAME_DIR + "df_crawled_terms.pickle")
    state.df_counts_by_hour = pd.read_pickle(DATAFRAME_DIR + "df_counts_by_hour.pickle")
    state.df_most_common_hashtags = pd.read_pickle(
        DATAFRAME_DIR + "df_most_common_hashtags.pickle"
    )
    state.df_most_common_tokens = pd.read_pickle(
        DATAFRAME_DIR + "df_most_common_tokens.pickle"
    )
    state.df_cooccurrence = pd.read_pickle(DATAFRAME_DIR + "df_cooccurrence.pickle")

    state.df_weekly_top_tweets = pd.read_pickle(DATAFRAME_DIR + "df_weekly_top_tweets.pickle")
    state.df_weekly_top_users = pd.read_pickle(DATAFRAME_DIR + "df_weekly_top_users.pickle")

    with open(DATAFRAME_DIR + "coverage_stats.pickle", "rb") as f:
        state.coverage_stats = pickle.load(f)
    print("Shared State Loaded")
    return state


shared_state = prepare_shared_state()
shared_state.selected_date = selected_date

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page(shared_state)
