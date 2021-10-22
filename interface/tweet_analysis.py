import streamlit as st
from data_tools import load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from .utils import (
    plot_hourly_coverage,
    plotly_hourly_coverage,
    lookup_parsed_tweet_data,
    get_most_common,
    create_crawled_terms_df,
)
import numpy as np
import seaborn as sns
from collections import Counter
from PIL import Image

# Plot styles
import matplotlib.style as style
import json
from collections import Counter

style.use("seaborn-poster")
style.use("ggplot")

LIMIT = None

CRAWLED_TERMS = load_crawled_terms("./keywords-3nov.txt")


def get_tweet_analysis_page(shared_state):
    st.header("Tweet Analysis")

    crawled_terms_df = shared_state.crawled_terms_df
    df_counts_by_hour = shared_state.df_counts_by_hour
    df_most_common_hashtags = shared_state.df_most_common_hashtags
    df_most_common_tokens = shared_state.df_most_common_tokens
    df_cooccurrence = shared_state.df_cooccurrence
    coverage_stats = shared_state.coverage_stats

    st.subheader("Basic stats & Coverage")
    start_time = pd.to_datetime(min(coverage_stats["earliest_tweet"], coverage_stats["earliest_retweet"]))
    end_time = pd.to_datetime(max(coverage_stats["latest_tweet"], coverage_stats["latest_retweet"]))
    st.markdown(
        """
        **Timespan:** {} to {}  
        **Number of tweets (excluding quote tweets):** {:,}  
        **Number of quote tweets:** {:,}  
        **Number of retweets:** {:,}  
        **Number of users:** {:,}

    """.format(
            start_time.strftime('%Y-%m-%d %H:%M'),
            end_time.strftime('%Y-%m-%d %H:%M'),
            coverage_stats["recent_tweet_count"] - coverage_stats["quote_tweet_count"],
            coverage_stats["quote_tweet_count"],
            coverage_stats["retweet_count"],
            coverage_stats["user_count"],
        )
    )
    st.subheader("Infomap Clustering (on 200k retweets)")
    infomap_img = Image.open("./interface/img/infomap-clustering.png")
    st.image(infomap_img, use_column_width=True)

    st.subheader("Hourly Coverage")
    show_hourly_ticks = st.checkbox("Show hourly ticks")
    st.plotly_chart(plotly_hourly_coverage(df_counts_by_hour, "retweet count", "Retweets", show_hourly_ticks))
    st.plotly_chart(plotly_hourly_coverage(df_counts_by_hour, "tweet count", "Tweets since Oct 23rd", show_hourly_ticks))

    col1, col2 = st.columns(2)
    col1.subheader("Most common hashtags")
    col1.dataframe(get_most_common(df_most_common_hashtags, "all tweets", 25))

    col2.subheader("Most common tokens")
    col2.dataframe(get_most_common(df_most_common_tokens, "all tweets", 25))

    st.subheader("All crawled terms (since 3rd of November)")

    st.dataframe(crawled_terms_df)

    st.subheader("Co-occurrence matrix (for terms with count > 5000)")

    st.dataframe(df_cooccurrence)

    co_occurrence_diagonal = np.diagonal(df_cooccurrence)

    with np.errstate(divide="ignore", invalid="ignore"):
        co_occurrence_fraction = np.nan_to_num(
            np.true_divide(df_cooccurrence, co_occurrence_diagonal[:, None])
        )

    fig = plt.figure()
    st.subheader("Co-occurence heatmap (inverted log-scaling)")
    st.markdown("Closer to 0 means higher correlation")
    with st.echo():
        co_occurrence_heatmap_df = pd.DataFrame(
            np.log(co_occurrence_fraction),
            index=df_cooccurrence.index,
            columns=df_cooccurrence.columns,
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


if __name__ == "__main__":
    get_tweet_analysis_page()
