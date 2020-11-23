import streamlit as st
from data_tools import load_parsed_data, load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from .utils import (
    plot_hourly_coverage,
    load_tweet_df,
    create_crawled_terms_df,
    lookup_parsed_tweet_data,
    load_df,
    most_common_hashtags,
)
import numpy as np
import seaborn as sns

# Plot styles
import matplotlib.style as style
import json

style.use("seaborn-poster")
style.use("ggplot")

CRAWLED_TERMS = load_crawled_terms("./keywords-3nov.txt")


def get_crawled_term_analysis_page(shared_state):
    st.header("Crawled term analysis")

    user_df = shared_state.user_df
    old_tweet_df = shared_state.old_tweet_df
    recent_tweet_df = shared_state.recent_tweet_df
    retweet_df = shared_state.retweet_df
    crawled_terms_df = shared_state.crawled_terms_df

    st.subheader("List of Crawled Terms (since 3rd of November)")

    st.dataframe(crawled_terms_df)

    crawled_term_threshold = st.number_input(
        "Exclude crawled terms under a certain threshold", value=5000, step=500
    )

    crawled_terms_df = crawled_terms_df[
        crawled_terms_df["tweet count"] > crawled_term_threshold
    ]

    st.markdown(
        "Filtered down to {} terms ({} in total)".format(
            len(crawled_terms_df.index), len(CRAWLED_TERMS)
        )
    )

    st.subheader("Co-occurrence matrix")

    terms_in_df = [term for term in crawled_terms_df["term"]]
    crawled_terms_tweet_df = (
        recent_tweet_df[terms_in_df].sparse.to_dense().astype("int32")
    )
    co_occurrence = crawled_terms_tweet_df.T.dot(crawled_terms_tweet_df)

    st.dataframe(co_occurrence)

    co_occurrence_diagonal = np.diagonal(co_occurrence)

    with np.errstate(divide="ignore", invalid="ignore"):
        co_occurrence_fraction = np.nan_to_num(
            np.true_divide(co_occurrence, co_occurrence_diagonal[:, None])
        )

    fig = plt.figure()
    st.subheader("Co-occurence heatmap (inverted log-scaling)")
    st.markdown("Closer to 0 means higher correlation")
    with st.echo():
        co_occurrence_heatmap_df = pd.DataFrame(
            np.log(co_occurrence_fraction),
            index=co_occurrence.index,
            columns=co_occurrence.columns,
        )
    np.fill_diagonal(co_occurrence_heatmap_df.values, np.nan)
    sns.heatmap(
        co_occurrence_heatmap_df,
        cbar=False,
        square=True,
        annot=True,
        vmin=-5,
        vmax=0,
        center=-2,
        cmap="PuBu",
        linecolor="black",
    )

    plt.tick_params(
        axis="both",
        which="major",
        labelsize=10,
        labelbottom=False,
        bottom=False,
        top=False,
        labeltop=True,
    )
    plt.xticks(rotation=45)
    st.pyplot(fig)

    selected_crawled_term = st.selectbox("Select term", crawled_terms_df["term"].values)

    if selected_crawled_term in recent_tweet_df.columns:
        filtered_by_crawled_term = recent_tweet_df[
            recent_tweet_df[selected_crawled_term] == 1
        ]
        st.pyplot(plot_hourly_coverage(filtered_by_crawled_term, selected_crawled_term))

    term_stats = (
        recent_tweet_df[recent_tweet_df[selected_crawled_term] == 1][
            ["retweet_count", "quote_count"]
        ]
        .fillna(0)
        .astype(int)
    )
    top_retweeted = term_stats.nlargest(10, "retweet_count").sort_values(
        "retweet_count", ascending=False
    )
    top_quoted = term_stats.nlargest(10, "quote_count").sort_values(
        "quote_count", ascending=False
    )
    st.subheader("Top hashtags for '{}'".format(selected_crawled_term))
    st.dataframe(most_common_hashtags(filtered_by_crawled_term, 15))

    st.subheader("10 randomly sampled tweets from '{}'".format(selected_crawled_term))
    st.table(
        pd.DataFrame(
            map(
                lambda t: [t["text"], t["quote_count"], t["retweet_count"]],
                lookup_parsed_tweet_data(
                    filtered_by_crawled_term.sample(n=10).index.values
                ),
            ),
            columns=["text", "quote_count", "retweet_count"],
        )
    )

    st.subheader("10 most retweeted tweets for '{}'".format(selected_crawled_term))
    st.table(
        pd.DataFrame(
            map(
                lambda t: [t["text"], t["quote_count"], t["retweet_count"]],
                lookup_parsed_tweet_data(top_retweeted.index.values),
            ),
            columns=["text", "quote_count", "retweet_count"],
        )
    )

    st.subheader("10 most quoted tweets for '{}'".format(selected_crawled_term))
    st.table(
        pd.DataFrame(
            map(
                lambda t: [t["text"], t["quote_count"], t["retweet_count"]],
                lookup_parsed_tweet_data(top_quoted.index.values),
            ),
            columns=["text", "quote_count", "retweet_count"],
        )
    )


if __name__ == "__main__":
    get_crawled_term_analysis_page()