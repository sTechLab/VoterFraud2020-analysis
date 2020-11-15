import streamlit as st
from data_tools import load_parsed_data


# @st.cache(allow_output_mutation=True)
def load_df(filename):
    return load_parsed_data(filename, verbose=True)


def get_tweet_analysis_page():
    st.header("Tweet Analysis")

    with st.spinner("Loading user data"):
        user_df = load_df("./data/14-nov/parsed_users.json")

    st.success("{:,} users loaded".format(len(user_df.index)))

    # with st.spinner("Loading tweet data"):
    #     tweet_df = load_df("./data/14-nov/parsed_tweets.json")

    # st.success("{:,} tweets loaded".format(len(tweet_df.index)))



    st.markdown(
        """
        **Number of tweets:** {}
        **Number of retweets:** {}
        **Number of users:** {}

    """.format(
            len(tweet_df.index),
            len(user_df.index),
            30
        )
    )


if __name__ == "__main__":
    get_tweet_analysis_page()
