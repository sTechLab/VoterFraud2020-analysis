import warnings
from data_tools import parse_dataflow_export, tokenize_tweet
from bs4 import MarkupResemblesLocatorWarning


warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)
def parse_tweet(tweet):
    cleaned_text, tokens, hashtags = tokenize_tweet(tweet["text"])
    tweet["cleaned_text"] = cleaned_text
    tweet["tokens"] = tokens
    tweet["hashtags"] = hashtags
    return tweet

tweet_directory = "./bucket-export/vote-safety-dataflow/14-nov/tweets/"
parse_dataflow_export(tweet_directory, "./data/test-2.json", parse_tweet)