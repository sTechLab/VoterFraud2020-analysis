import streamlit as st
import pandas as pd
import os, re
from interface.landing_page import get_landing_page
from interface.retweet_graph_analysis import get_retweet_graph_analysis_page
from interface.top_image_analysis import get_top_image_analysis_page
from interface.candidate_analysis import get_candidate_analysis_page
from interface.explore_data import get_explore_data_page
import interface.SessionState as SessionState
from interface.df_utils import load_pickled_df
from interface.image_urls import bucket_image_urls
import pickle5 as pickle

st.set_page_config(
    page_title="VoterFraud2020 - a Twitter Dataset of Election Fraud Claims",
    page_icon="./interface/img/favicon.ico",
    # layout = 'wide',
    initial_sidebar_state="expanded",
)


@st.cache
def insert_html_header(name, snippet):
    a = os.path.dirname(st.__file__) + "/static/index.html"
    with open(a, "r") as f:
        data = f.read()
        if snippet not in data:
            print("Inserting {}".format(name))
            with open(a, "w") as ff:
                new_data = re.sub("<head>", "<head>" + snippet, data)
                ff.write(new_data)
        else:
            print("{} already inserted".format(name))


## Google analytics
insert_html_header(
    "Google Analytics Tag",
    """
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8VB4WZRD7C"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-8VB4WZRD7C');
</script>
""",
)

insert_html_header(
    "Meta tags",
    """
<!-- Primary Meta Tags -->
<title>VoterFraud2020 - a Twitter Dataset of Election Fraud Claims</title>
<meta name="title" content="VoterFraud2020 - a Twitter Dataset of Election Fraud Claims">
<meta name="description" content="Voterfraud2020 is a multi-modal Twitter dataset with 7.6M tweets and 25.6M retweets from 2.6M users related to voter fraud claims.">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://metatags.io/">
<meta property="og:title" content="VoterFraud2020 - a Twitter Dataset of Election Fraud Claims">
<meta property="og:description" content="Voterfraud2020 is a multi-modal Twitter dataset with 7.6M tweets and 25.6M retweets from 2.6M users related to voter fraud claims.">
<meta property="og:image" content="{}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://metatags.io/">
<meta property="twitter:title" content="VoterFraud2020 - a Twitter Dataset of Election Fraud Claims">
<meta property="twitter:description" content="Voterfraud2020 is a multi-modal Twitter dataset with 7.6M tweets and 25.6M retweets from 2.6M users related to voter fraud claims.">
<meta property="twitter:image" content="{}">
""".format(
        bucket_image_urls["retweet_graph_suspended"],
        bucket_image_urls["retweet_graph_suspended"],
    ),
)

query_params = st.experimental_get_query_params()
app_state = st.experimental_get_query_params()

session_state = SessionState.get(first_query_params=query_params)
first_query_params = session_state.first_query_params

PAGES = {
    "VoterFraud2020": get_landing_page,
    "Retweet Graph Analysis": get_retweet_graph_analysis_page,
    "Explore The Dataset": get_explore_data_page,
    "Top Images": get_top_image_analysis_page,
    "Midterm Candidates": get_candidate_analysis_page,
    # "Overview": get_tweet_analysis_page,
    # "Top Tweets": get_weekly_tweet_analysis_page,
    # "Top Users": get_weekly_user_analysis_page,
    # "URL Analysis": get_url_analysis_page,
    # "Filter by crawled term": get_crawled_term_analysis_page,
}
PAGE_OPTIONS = list(PAGES.keys())

LIMIT = None


class SharedState:
    pass


DATAFRAME_DIR = "./interface/data/"


@st.cache(allow_output_mutation=True)
def prepare_shared_state():
    print("Preparing Shared State")
    state = SharedState()

    # with st.spinner("Loading user data"):
    #    state.user_df = pd.read_pickle(DATAFRAME_DIR + "df_users.pickle")

    # state.crawled_terms_df = pd.read_pickle(DATAFRAME_DIR + "df_crawled_terms.pickle")

    state.df_images_promoters = pd.read_csv(
        "./interface/data/top_10_retweeted_promoters.csv", delimiter=";"
    ).drop("Unnamed: 0", axis=1)[
        [
            "num_of_unique_tweet_id",
            "sum_of_retweets_by_cluster_1_to_4",
            "sum_of_retweet_count",
            "image_url",
        ]
    ]

    state.df_candidates = pd.read_pickle("./interface/data/candidate_users.pickle")
    state.df_candidates["user_community"] = state.df_candidates[
        "user_community"
    ].astype(object)

    state.df_images_detractors = pd.read_csv(
        "./interface/data/top_10_retweeted_detractors.csv", delimiter=";"
    ).drop("Unnamed: 0", axis=1)[
        [
            "num_of_unique_tweet_id",
            "retweets_by_cluster_0",
            "sum_of_retweet_count",
            "image_url",
        ]
    ]

    state.df_images_suspended = pd.read_csv(
        "./interface/data/top_10_retweeted_suspended.csv", delimiter=";"
    ).drop("Unnamed: 0", axis=1)[
        [
            "num_of_unique_tweet_id",
            "retweets_by_suspended",
            "sum_of_retweet_count",
            "image_url",
        ]
    ]
    # state.df_most_common_hashtags = pd.read_pickle(
    #     DATAFRAME_DIR + "df_most_common_hashtags.pickle"
    # )
    # state.df_most_common_tokens = pd.read_pickle(
    #     DATAFRAME_DIR + "df_most_common_tokens.pickle"
    # )
    # state.df_cooccurrence = pd.read_pickle(DATAFRAME_DIR + "df_cooccurrence.pickle")

    # state.df_weekly_top_tweets = pd.read_pickle(
    #     DATAFRAME_DIR + "df_weekly_top_tweets.pickle"
    # )
    # state.df_weekly_top_users = pd.read_pickle(
    #     DATAFRAME_DIR + "df_weekly_top_users.pickle"
    # )

    with open(DATAFRAME_DIR + "coverage_stats.pickle", "rb") as f:
        state.coverage_stats = pickle.load(f)
    print("Shared State Loaded")
    return state


def get_selected_page_index():
    # query_params = st.experimental_get_query_params()
    if "page" in app_state:
        if "page" in first_query_params:
            selected_page = first_query_params["page"][0]
            if selected_page in PAGE_OPTIONS:
                return PAGE_OPTIONS.index(selected_page)
    return 0


shared_state = prepare_shared_state()

## CSS
st.markdown(
    """
    <style>
    img.logo {
        margin: 0px auto;
        margin-top: -45px;
        margin-bottom: 25px;
        width: 200px;
    }

    img.logo-2 {
        margin: 0px auto;
        margin-top: 25px;
        width: 200px;
    }

    img {
        max-width: 100%;
    }
    </style>
""",
    unsafe_allow_html=True,
)


st.sidebar.markdown(
    """
    <img src="{}" class="logo" alt="CT logo" />
""".format(
        bucket_image_urls["jacobs-logo-transparent"]
    ), unsafe_allow_html=True
)


st.sidebar.title("Navigation")

selection = st.sidebar.radio("Go to", PAGE_OPTIONS, index=get_selected_page_index())

st.sidebar.markdown(
    """
    - [The Paper (arXiv)](https://arxiv.org/abs/2101.08210)

    ### Download The Full Dataset
    - [Github Repository](https://github.com/sTechLab/VoterFraud2020)  
    - [Fighshare](https://doi.org/10.6084/m9.figshare.13571084)
"""
)

# st.sidebar.markdown(
#     """
#     <img src="{}" class="logo-2" alt="Jacobs logo" />
# """.format(
#         bucket_image_urls["jacobs-logo-transparent"]
#     ), unsafe_allow_html=True
# )

app_state["page"] = selection


def get_query_params():
    if PAGE_OPTIONS.index(selection) == 0:
        return {}
    else:
        return {"page": app_state["page"]}


st.experimental_set_query_params(**get_query_params())

page = PAGES[selection]
page(shared_state)

