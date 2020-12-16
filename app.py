import streamlit as st
from interface.tweet_analysis import get_tweet_analysis_page
from interface.crawled_term_analysis import get_crawled_term_analysis_page
from interface.user_analysis import get_user_analysis_page
from interface.url_analysis import get_url_analysis_page
from interface.utils import (
    load_user_df,
    load_tweet_df,
    load_retweet_df,
    create_crawled_terms_df,
)
from data_tools import load_crawled_terms

PAGES = {
    "Tweet Analysis": get_tweet_analysis_page,
    "User Analysis": get_user_analysis_page,
    "URL Analysis": get_url_analysis_page,
    "Filter by crawled term": get_crawled_term_analysis_page,
}

LIMIT = None
CRAWLED_TERMS = load_crawled_terms("./keywords-3nov.txt")


class SharedState:
    pass


@st.cache(allow_output_mutation=True)
def prepare_shared_state():
    print("Preparing Shared State")
    state = SharedState()

    with st.spinner("Loading user data"):
        state.user_df = load_user_df()

    with st.spinner("Loading retweet data"):
        state.retweet_df = load_retweet_df()

    with st.spinner("Loading tweet data"):
        old_tweet_df, recent_tweet_df = load_tweet_df(
            state.retweet_df.timestamp.min(), CRAWLED_TERMS
        )

        state.old_tweet_df = old_tweet_df
        state.recent_tweet_df = recent_tweet_df

    state.crawled_terms_df = create_crawled_terms_df(CRAWLED_TERMS, recent_tweet_df)

    return state


shared_state = prepare_shared_state()

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page(shared_state)
