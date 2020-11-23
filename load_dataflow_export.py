import warnings
from data_tools import parse_dataflow_export, tokenize_tweet, load_crawled_terms
from bs4 import MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

crawled_terms = load_crawled_terms("./keywords-3nov.txt")
lowered_crawled_terms = [term.lower() for term in crawled_terms]


def parse_str_to_int(s):
    return int(s) if s.isdigit() else 0


def parse_tweet(tweet):
    cleaned_text, tokens, hashtags, entities = tokenize_tweet(tweet["text"])
    # tweet["cleaned_text"] = cleaned_text
    tweet["tokens"] = tokens
    tweet["hashtags"] = hashtags
    tweet["entities"] = entities

    tweet["retweet_count"] = parse_str_to_int(tweet["retweet_count"])
    if "quote_count" in tweet:
        tweet["quote_count"] = parse_str_to_int(tweet["quote_count"])
    else:
        tweet["quote_count"] = 0

    # Drop irrelevant columns
    del tweet["sha256"]
    del tweet["source"]
    del tweet["coordinates"]
    del tweet["processed"]
    del tweet["media"]
    del tweet["place"]

    lowered_tweet_text = tweet["text"].lower()

    for term in lowered_crawled_terms:
        if term[0] == "#":
            lower_term_without_hashtag = term[1:]
            for hashtag in tweet["hashtags"]:
                if lower_term_without_hashtag == hashtag.lower():
                    tweet[term] = 1
                    break
        elif term in lowered_tweet_text:
            tweet[term] = 1
    return tweet


EXPORT_TAG = "14-nov"

data_sources = [
    # {"type": "retweets"},
    # {"type": "users"},
    # {"type": "media"},
    # {"type": "hashtag"},
    {"type": "tweets", "parser": parse_tweet},
]


for data_source in data_sources:
    data_type = data_source["type"]
    data_parser = data_source["parser"] if "parser" in data_source else None

    data_directory = "./bucket-export/vote-safety-dataflow/{}/{}/".format(
        EXPORT_TAG, data_type
    )
    parse_dataflow_export(
        data_directory,
        "./data/{}/parsed_{}.json".format(EXPORT_TAG, data_type),
        data_parser,
    )
