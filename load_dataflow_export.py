import warnings
from data_tools import parse_dataflow_export, tokenize_tweet, load_crawled_terms
from bs4 import MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

crawled_terms = load_crawled_terms("./keywords-3nov.txt")

def parse_tweet(tweet):
    cleaned_text, tokens, hashtags = tokenize_tweet(tweet["text"])
    tweet["cleaned_text"] = cleaned_text
    tweet["tokens"] = tokens
    tweet["hashtags"] = hashtags

    for term in crawled_terms:
        if (term in cleaned_text):
            tweet[term] = 1
        else:
            tweet[term] = 0
    return tweet


EXPORT_TAG = "14-nov"

data_sources = [
    {"type": "tweets", "parser": parse_tweet},
    #{"type": "retweets"},
    #{"type": "users"},
    #{"type": "media"},
    #{"type": "hashtag"},
]


for data_source in data_sources:
    data_type = data_source["type"]
    data_parser = data_source["parser"] if "parser" in data_source else None

    data_directory = "./bucket-export/vote-safety-dataflow/{}/{}/".format(
        EXPORT_TAG, data_type
    )
    parse_dataflow_export(
        data_directory, "./data/{}/parsed_{}.json".format(EXPORT_TAG, data_type), data_parser
    )
