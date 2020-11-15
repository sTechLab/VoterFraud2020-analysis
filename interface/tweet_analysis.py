import streamlit as st
from data_tools import load_parsed_data, load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from .utils import plot_hourly_coverage
import numpy as np
# Plot styles
import matplotlib.style as style

style.use("seaborn-poster")
style.use("ggplot")

LIMIT = None

@st.cache(allow_output_mutation=True)
def load_df(filename, include_cols=None, exclude_cols={}, limit=None):
    return load_parsed_data(
        filename,
        include_cols=include_cols,
        exclude_cols=exclude_cols,
        verbose=True,
        limit=limit,
    )


def create_crawled_terms_df(crawled_terms, tweet_df):
    crawled_terms_stats = []

    for term in crawled_terms:
        if term in tweet_df.columns:
            stats = {}
            stats["term"] = term
            stats["tweet count"] = tweet_df[term].value_counts().values[0]
            crawled_terms_stats.append(stats)

    crawled_terms_df = pd.DataFrame(crawled_terms_stats).sort_values(
        by=["tweet count"], ascending=False
    )

    return crawled_terms_df


def get_tweet_analysis_page():
    st.header("Tweet Analysis")

    with st.spinner("Loading user data"):
        user_df = load_df(
            "./data/14-nov/parsed_users.json",
            exclude_cols={"description"},
            limit=LIMIT,
        )

    with st.spinner("Loading tweet data"):
        tweet_df = load_df(
            "./data/14-nov/parsed_tweets.json",
            exclude_cols={
                "tokens",
                "cleaned_text",
                "text",
                "last_retweeted",
                "place",
                "processed",
                "media",
                "isDeleted",
            },
            limit=LIMIT,
        )

    with st.spinner("Loading retweet data"):
        retweet_df = load_df(
            "./data/14-nov/parsed_retweets.json",
            exclude_cols={"tokens", "cleaned_text", "text", "last_retweeted"},
            limit=LIMIT,
        )
        recent_tweet_df = tweet_df[tweet_df.timestamp > "2020-10-23 00:00:00"]

    crawled_terms = load_crawled_terms("./keywords-3nov.txt")

    st.subheader("Basic stats")
    st.markdown(
        """
        **Number of tweets:** {}  
        **Number of tweets after October 23rd:** {}  
        **Number of retweets:** {}  
        **Number of users:** {}

    """.format(
            len(tweet_df.index),
            len(recent_tweet_df.index),
            len(retweet_df.index),
            len(user_df.index),
        )
    )

    st.subheader("Coverage")
    st.markdown(
        """
        **Earliest tweet:** {}  
        **Latest tweet:** {}  
        **Earliest retweet:** {}  
        **Latest retweet:** {}  

    """.format(
            tweet_df.timestamp.min(),
            tweet_df.timestamp.max(),
            retweet_df.timestamp.min(),
            retweet_df.timestamp.max(),
        )
    )

    st.subheader("Hourly Coverage")
    st.pyplot(plot_hourly_coverage(retweet_df, "Retweets"))
    st.pyplot(plot_hourly_coverage(recent_tweet_df, "Tweets since Oct 23rd"))

    st.subheader("Crawled terms (since 3rd of November)")

    crawled_terms_df = create_crawled_terms_df(crawled_terms, tweet_df)
    st.dataframe(crawled_terms_df)

    selected_crawled_term = st.selectbox("Select term", crawled_terms)

    if selected_crawled_term in tweet_df.columns:
        filtered_by_crawled_term = tweet_df[tweet_df[selected_crawled_term] == 1]
        st.pyplot(plot_hourly_coverage(filtered_by_crawled_term, selected_crawled_term))

    st.subheader("Co-occurrence matrix")

    terms_in_df = [term for term in crawled_terms if term in tweet_df.columns]
    crawled_terms_tweet_df = tweet_df[terms_in_df].fillna(0).astype(int)
    co_occurrence = crawled_terms_tweet_df.T.dot(crawled_terms_tweet_df)

    st.dataframe(co_occurrence)


    co_occurrence_diagonal = np.diagonal(co_occurrence)

    with np.errstate(divide='ignore', invalid='ignore'):
        co_occurrence_percentage = np.nan_to_num(np.true_divide(co_occurrence, co_occurrence_diagonal[:, None]))

    
    st.subheader("Co-occurence matrix (log percentage)")
    st.dataframe(np.log(co_occurrence_percentage))
    

if __name__ == "__main__":
    get_tweet_analysis_page()
