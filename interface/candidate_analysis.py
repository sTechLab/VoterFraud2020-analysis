import streamlit as st
from collections import defaultdict
import pandas as pd
import numpy as np

CLUSTER_PROMOTERS = "Promoters of Voter Fraud Claims"
CLUSTER_DETRACTORS = "Detractors of Voter Fraud Claims"
CLUSTER_SUSPENDED = "Suspended Users"


def get_candidate_analysis_page(shared_state):
    df_candidates = shared_state.df_candidates
    st.header("Midterm Candidates")
    st.markdown(
        """
        This page shows statistics for the Twitter accounts of midterm election candidates that appear in the VoterFraud2020 dataset. 
        For comparison, Donald Trump's account (@realDonaldTrump) was also added. 

        The list of Twitter accounts was obtained from [this paper](https://arxiv.org/abs/2005.04412).

    """
    )

    col1, col2 = st.beta_columns(2)

    filter_by_community = col1.multiselect("Filter by community", [0, 1, 2])
    filter_by_party = col2.multiselect(
        "Filter by political party", ["Democratic", "Republican"]
    )
    sort_by_column = st.selectbox(
        "Sort by column",
        [
            "followers_count",
            "retweet_count_by_detractors",
            "retweet_count_by_promoters",
            "retweet_count_by_suspended_users",
        ],
    )
    filtered_df = df_candidates
    if len(filter_by_community) > 0:
        filtered_df = filtered_df[
            filtered_df.user_community.isin(filter_by_community)
        ]

    if len(filter_by_party) > 0:
        filtered_df = filtered_df[
            filtered_df.party.isin(filter_by_party)
        ]

    filtered_df = filtered_df.sort_values(sort_by_column, ascending=False)

    st.markdown(
        """
        *{} accounts ({} suspended)*
    """.format(
            filtered_df.shape[0],
            filtered_df[filtered_df.user_active_status == "suspended"].shape[0],
        )
    )
    st.table(
        filtered_df.reset_index()
        .assign(hack="")
        .drop(["state", "position"], axis=1)
        .set_index("hack")
    )


if __name__ == "__main__":
    get_candidate_analysis_page()
