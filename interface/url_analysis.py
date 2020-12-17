import streamlit as st
from data_tools import load_crawled_terms
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict
import pandas as pd
import numpy as np
import heapq

# Plot styles
import matplotlib.style as style
import json

style.use("seaborn-poster")
style.use("ggplot")

LIMIT = None


def load_url_map(path, selected_date):
    directory = "./notebooks/data_export/url_stats/"
    if selected_date == "16-dec":
        directory += selected_date + "/"
    with open("{}{}.json".format(directory, path)) as json_file:
        url_map = json.load(json_file)
        unique_tweet_ids = set()

        total_tweet_count = 0
        total_retweet_count = 0
        total_quote_count = 0

        for key, url in url_map.items():
            unique_tweet_ids.update(url["tweet_ids"])
            total_quote_count += url["aggregated_quote_count"]
            total_retweet_count += url["aggregated_retweet_count"]
        return (
            url_map,
            {
                "total_tweet_count": len(unique_tweet_ids),
                "total_retweet_count": total_retweet_count,
                "total_quote_count": total_quote_count,
            },
        )


def top_urls_by_retweet_count(url_map, N=10):
    top_urls = []
    for url in heapq.nlargest(
        N, url_map, key=lambda x: url_map.get(x)["aggregated_retweet_count"]
    ):
        url_stats = url_map.get(url)
        tweet_count = len(url_stats["tweet_ids"])

        top_urls.append(
            {
                "url": url,
                "retweet_count": url_stats["aggregated_retweet_count"],
                "tweet_count": tweet_count,
                "quote_count": url_stats["aggregated_quote_count"],
            }
        )
    return top_urls


def get_url_analysis_page(shared_state):
    st.header("URL Analysis")

    selected_date = shared_state.selected_date

    url_map, url_stats = load_url_map("all_urls", selected_date)

    st.subheader("URL Stats")
    st.markdown(
        """
        **Number of tweets with URLs:** {:,}  
        **Unique URLs shared:** {:,}  
        **URL share retweet count:** {:,}  
        **URL share quote count:** {:,}
    """.format(
            url_stats["total_tweet_count"],
            len(url_map.keys()),
            url_stats["total_retweet_count"],
            url_stats["total_quote_count"],
        )
    )

    st.subheader("Top URLs by retweet count")
    st.table(top_urls_by_retweet_count(url_map))

    youtube_url_map, _ = load_url_map("youtube_urls", selected_date)
    st.subheader("Top Youtube URLs by retweet count")
    st.write("Youtube URLs in the dataset: {:,}".format(len(youtube_url_map.keys())))
    st.table(top_urls_by_retweet_count(youtube_url_map))

    domain_url_map, _ = load_url_map("domains", selected_date)
    st.subheader("Top domains by retweet count")
    st.write("Domains in the dataset: {:,}".format(len(domain_url_map.keys())))
    st.table(top_urls_by_retweet_count(domain_url_map))


if __name__ == "__main__":
    get_url_analysis_page()
