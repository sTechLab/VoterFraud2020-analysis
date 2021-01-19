import streamlit as st
import pandas as pd

# from interface.tweet_analysis import get_tweet_analysis_page
# from interface.url_analysis import get_url_analysis_page

# from interface.crawled_term_analysis import get_crawled_term_analysis_page
#from interface.weekly_user_analysis import get_weekly_user_analysis_page
#from interface.weekly_tweet_analysis import get_weekly_tweet_analysis_page
from interface.landing_page import get_landing_page
from interface.retweet_graph_analysis import get_retweet_graph_analysis_page
from interface.top_image_analysis import get_top_image_analysis_page
from interface.explore_data import get_explore_data_page
import interface.SessionState as SessionState
import pickle

query_params = st.experimental_get_query_params()
app_state = st.experimental_get_query_params()

session_state = SessionState.get(first_query_params=query_params)
first_query_params = session_state.first_query_params

st.set_page_config(
    page_title="VoterFraud2020",
    # page_icon = favicon,
    # layout = 'wide',
    initial_sidebar_state="expanded",
)

PAGES = {
    "VoterFraud2020": get_landing_page,
    "Retweet Graph Analysis": get_retweet_graph_analysis_page,
    "Explore The Dataset": get_explore_data_page,
    "Top Images": get_top_image_analysis_page,
    # "Overview": get_tweet_analysis_page,
    #"Top Tweets": get_weekly_tweet_analysis_page,
    #"Top Users": get_weekly_user_analysis_page,
    # "URL Analysis": get_url_analysis_page,
    # "Filter by crawled term": get_crawled_term_analysis_page,
}
PAGE_OPTIONS = list(PAGES.keys())

LIMIT = None


class SharedState:
    pass


selected_date = "16-dec"
# selected_date = st.selectbox("Select dataset", ["14-nov", "16-dec"], index=1)
DATAFRAME_DIR = "./data/dataframes/{}/".format(selected_date)


@st.cache(allow_output_mutation=True)
def prepare_shared_state():
    print("Preparing Shared State")
    state = SharedState()

    # with st.spinner("Loading user data"):
    #    state.user_df = pd.read_pickle(DATAFRAME_DIR + "df_users.pickle")

    # state.crawled_terms_df = pd.read_pickle(DATAFRAME_DIR + "df_crawled_terms.pickle")
    state.df_counts_by_hour = pd.read_pickle(DATAFRAME_DIR + "df_counts_by_hour.pickle")
    state.df_most_common_hashtags = pd.read_pickle(
        DATAFRAME_DIR + "df_most_common_hashtags.pickle"
    )
    state.df_most_common_tokens = pd.read_pickle(
        DATAFRAME_DIR + "df_most_common_tokens.pickle"
    )
    state.df_cooccurrence = pd.read_pickle(DATAFRAME_DIR + "df_cooccurrence.pickle")

    state.df_weekly_top_tweets = pd.read_pickle(
        DATAFRAME_DIR + "df_weekly_top_tweets.pickle"
    )
    state.df_weekly_top_users = pd.read_pickle(
        DATAFRAME_DIR + "df_weekly_top_users.pickle"
    )

    with open(DATAFRAME_DIR + "coverage_stats.pickle", "rb") as f:
        state.coverage_stats = pickle.load(f)
    print("Shared State Loaded")
    return state


def get_selected_page_index():
    #query_params = st.experimental_get_query_params()
    if "page" in app_state:
        if "page" in first_query_params:
            selected_page = first_query_params["page"][0]
            if selected_page in PAGE_OPTIONS:
                return PAGE_OPTIONS.index(selected_page)
    return 0


shared_state = prepare_shared_state()
shared_state.selected_date = selected_date

st.sidebar.title("Navigation")

selection = st.sidebar.radio(
    "Go to", PAGE_OPTIONS, index=get_selected_page_index()
)

st.sidebar.markdown("""
    - [The Paper (PDF)]()

    ### Download The Dataset
    - [Github Repository](https://github.com/sTechLab/VoterFraud2020)  
    - [Fighshare](https://doi.org/10.6084/m9.figshare.13571084)
""")

# if (PAGE_OPTIONS.index(selection) == 0):
#     if ("page" in app_state):
#         del app_state["page"]
# else:
app_state["page"] = selection

st.experimental_set_query_params(**app_state)

page = PAGES[selection]
page(shared_state)
