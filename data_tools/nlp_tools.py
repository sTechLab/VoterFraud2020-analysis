from bs4 import BeautifulSoup
import re
import spacy
import string

parser = spacy.load("en_core_web_lg")

# remove punctuation

FORBIDDEN_SYMBOLS = [
    "C",
    "k",
    "🇸",
    "c",
    "b",
    "t",
    "K",
    "L",
    "Q",
    "s",
    "x",
    "F",
    "️",
    "l",
    "j",
    "°",
    "U",
    "J",
    "n",
    "G",
    "A",
    "P",
    "w",
    "E",
    "H",
    "D",
    "R",
    "Y",
    "🇱",
    "f",
    "B",
    "v",
    "e",
    "u",
    "m",
    "r",
    "q",
    "’",
    "O",
    "™",
    "g",
    "p",
    "\u2060",
    "d",
    "V",
    "I",
    "X",
    "h",
    "y",
    "W",
    "S",
    "🇧",
    "o",
    "N",
]

PUNCTUATION = set(string.punctuation)
PUNCTUATION.update(set(FORBIDDEN_SYMBOLS))


def doc2token(txt):

    escape_punct_re = re.compile("[%s]" % re.escape(string.punctuation))
    escape_punct = lambda x: escape_punct_re.sub("", x)

    parsed = parser(txt, disable=["tagger", "parser", "entity", "ner", "textcat"])
    tokens = list()
    for token in parsed:
        # if token.is_punct or token.is_digit:
        #    continue
        if token.lemma_ in PUNCTUATION:
            continue
        # if token.lemma_=='-PRON-':
        #    continue
        else:
            tokens.append(escape_punct(token.lemma_.lower()).strip())
    return tokens

RE_PATTERNS = {
    "url": re.compile("http(.+)?(\W|$)"),
    "spacing": re.compile("[\n\r\t ]+"),
    "leading_mention": "^(\.?@\w+([^\w]|$))+",
    "mention": "@(\w+)",
    "hashtag": "#(\w+)"
}


def tokenize_tweet(x):
    # preprocess

    unescape_html = (
        lambda x: BeautifulSoup(x, features="html.parser").get_text().strip()
    )
    remove_urls = lambda x: re.sub(RE_PATTERNS["url"], " ", x)

    normalize_spaces = lambda x: re.sub(RE_PATTERNS["spacing"], " ", x)

    remove_leading_mentions = lambda x: re.sub(RE_PATTERNS["leading_mention"], "", x)
    # remove_emoji = lambda x: demoji.replace(x, " ")

    encodeMention = lambda x: re.sub(RE_PATTERNS["mention"], "mention\g<1>", x)
    encodeHashtag = lambda x: re.sub(RE_PATTERNS["hashtag"], "hashtag\g<1>", x)

    cleaned_text = encodeHashtag(
        encodeMention(
            remove_leading_mentions(normalize_spaces(remove_urls(unescape_html(x))))
        )
    ) 

    tokens = doc2token(cleaned_text)
    hashtags = re.findall(RE_PATTERNS["hashtag"], x)
    return cleaned_text, tokens, hashtags

