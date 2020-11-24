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
    "”",
    "“",
    "🇺",
]

PUNCTUATION = set(string.punctuation)
PUNCTUATION.update(set(FORBIDDEN_SYMBOLS))
escape_punct_re = re.compile("[%s]" % re.escape(string.punctuation))

INCLUDE_ENTITIES = False

spacy_disabled_modules = ["tagger", "parser", "entity", "textcat"]

if not INCLUDE_ENTITIES:
    spacy_disabled_modules.append("ner")


def doc2tokens(txt):
    escape_punct = lambda x: escape_punct_re.sub("", x)
    parsed = parser(txt, disable=spacy_disabled_modules)
    tokens = list()
    entities = list()
    urls = list()

    for token in parsed:
        if token.like_url:
            urls.append(token.text)
        elif token.lemma_ in PUNCTUATION or token.lemma_ == "-PRON-":
            continue
        else:
            tokens.append(escape_punct(token.lemma_.lower()).strip())

    if INCLUDE_ENTITIES:
        for ent in parsed.ents:
            if ent.label_ in {
                "PERSON",
                "NORP",
                "FAC",
                "ORG",
                "GPE",
                "LOC",
                "PRODUCT",
                "EVENT",
                "WORK_OF_ART",
                "LAW",
            }:
                entities.append(ent.text)

    return tokens, entities, urls


RE_PATTERNS = {
    "spacing": re.compile("[\n\r\t ]+"),
    "leading_mention": "^(\.?@\w+([^\w]|$))+",
    "mention": "@(\w+)",
    "hashtag": "#(\w+)",
}


def tokenize_tweet(x):
    # preprocess

    unescape_html = (
        lambda x: BeautifulSoup(x, features="html.parser").get_text().strip()
    )

    normalize_spaces = lambda x: re.sub(RE_PATTERNS["spacing"], " ", x)

    remove_leading_mentions = lambda x: re.sub(RE_PATTERNS["leading_mention"], "", x)

    encodeMention = lambda x: re.sub(RE_PATTERNS["mention"], "mention\g<1>", x)
    encodeHashtag = lambda x: re.sub(RE_PATTERNS["hashtag"], "hashtag\g<1>", x)

    cleaned_text = encodeHashtag(
        encodeMention(remove_leading_mentions(normalize_spaces(unescape_html(x))))
    )

    tokens, entities, urls = doc2tokens(cleaned_text)
    hashtags = re.findall(RE_PATTERNS["hashtag"], x)

    return cleaned_text, tokens, hashtags, entities, urls

