import streamlit as st
from data_tools import load_parsed_data, load_crawled_terms


@st.cache(allow_output_mutation=True)
def load_df(filename, exclude_cols={}, limit=None):
    return load_parsed_data(filename, exclude_cols, verbose=True, limit=limit)


def get_tweet_analysis_page():
    st.header("Tweet Analysis")

    with st.spinner("Loading user data"):
        user_df = load_df(
            "./data/14-nov/parsed_users.json", exclude_cols={"description"}, limit=10000
        )

    with st.spinner("Loading tweet data"):
        tweet_df = load_df(
            "./data/14-nov/parsed_tweets.json",
            include_cols={
                "tokens",
                "cleaned_text",
                "text",
                "last_retweeted",
                "place",
                "processed",
                "media",
                "isDeleted",
            },
            limit=10000,
        )

    with st.spinner("Loading retweet data"):
        retweet_df = load_df(
            "./data/14-nov/parsed_retweets.json",
            exclude_cols={"tokens", "cleaned_text", "text", "last_retweeted"},
            limit=10000,
        )

    crawled_terms = load_crawled_terms("./keywords-3nov.txt")

    st.subheader("Crawled terms")
    st.dataframe(crawled_terms)

    st.markdown(
        """
        **Number of tweets:** {}  
        **Number of retweets:** {}  
        **Number of users:** {}

    """.format(
            len(tweet_df.index), len(retweet_df.index), len(user_df.index)
        )
    )


if __name__ == "__main__":
    get_tweet_analysis_page()
