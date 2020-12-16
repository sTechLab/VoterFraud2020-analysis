import streamlit as st
import pandas as pd
from interface.tweet_analysis import get_tweet_analysis_page
from interface.crawled_term_analysis import get_crawled_term_analysis_page
from interface.user_analysis import get_user_analysis_page
from interface.url_analysis import get_url_analysis_page

PAGES = {
    "Tweet Analysis": get_tweet_analysis_page,
    "User Analysis": get_user_analysis_page,
    "URL Analysis": get_url_analysis_page,
    "Filter by crawled term": get_crawled_term_analysis_page,
}

LIMIT = None
DATAFRAME_DIR = './data/dataframes/14-nov/'

class SharedState:
    pass


@st.cache(allow_output_mutation=True)
def prepare_shared_state():
    print("Preparing Shared State")
    state = SharedState()

    with st.spinner("Loading user data"):
        state.user_df = pd.read_pickle(DATAFRAME_DIR + 'df_users.pickle')

    with st.spinner("Loading retweet data"):
        state.retweet_df = pd.read_pickle(DATAFRAME_DIR + 'df_retweets.pickle')

    with st.spinner("Loading tweet data"):
        state.old_tweet_df = pd.read_pickle(DATAFRAME_DIR + 'df_old_tweets.pickle')
        state.recent_tweet_df = pd.read_pickle(DATAFRAME_DIR + 'df_recent_tweets.pickle')
    state.crawled_terms_df = pd.read_pickle(DATAFRAME_DIR + 'df_crawled_terms.pickle')
    state.df_counts_by_hour = pd.read_pickle(DATAFRAME_DIR + 'df_counts_by_hour.pickle')
    state.df_most_common_hashtags = pd.read_pickle(DATAFRAME_DIR + 'df_most_common_hashtags.pickle')
    state.df_cooccurrence = pd.read_pickle(DATAFRAME_DIR + 'df_cooccurrence.pickle')

    return state


shared_state = prepare_shared_state()

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page(shared_state)
