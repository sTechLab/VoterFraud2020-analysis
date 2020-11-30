def load_tweet_df():
    from data_tools import load_crawled_terms, load_parsed_data

    crawled_terms, crawled_hashtags, crawled_phrases = load_crawled_terms("../keywords-3nov.txt", split_hashtags=True)

    cast_cols = {
        "tweet_count": "int32",
        "quote_count": "int32" 
    }
    for term in crawled_terms:
        cast_cols[term] = "Sparse[int8]"

    tweet_df = load_parsed_data('../data/14-nov/parsed_tweets.json', exclude_cols={
        "cleaned_text", 
        "entities",
        "replyTo",
        "replyTo_user",
        "text", 
        "last_retweeted", 
        "place", 
        "processed",
        "media", 
        "isDeleted"
    }, cast_cols=cast_cols, verbose=True)

    recent_tweet_df = tweet_df[tweet_df.timestamp > '2020-10-23 00:00:00']

    return tweet_df, recent_tweet_df

def setup_styles():
    # Plot styles
    import matplotlib.style as style
    style.use('seaborn-poster')
    style.use('ggplot')

def resolve_paths_from_parent_directory():
    # Resolve paths from root project directory
    import os
    import sys
    module_path = os.path.abspath(os.path.join('..'))
    if module_path not in sys.path:
        sys.path.append(module_path)

def setup():
    resolve_paths_from_parent_directory()
    setup_styles()