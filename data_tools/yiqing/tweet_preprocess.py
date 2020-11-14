import json
from collections import defaultdict
import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from matplotlib.patches import Rectangle
import datetime
import time
from collections import Counter
import os
from bs4 import BeautifulSoup
#import networkx as nx
import random
import hashlib
import re
import math
import copy

import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models
from pprint import pprint

from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
from nltk import TweetTokenizer
import numpy as np
import torch

from sklearn.utils.extmath import randomized_svd
from gensim.models.phrases import Phrases, Phraser

import pickle
import string

import spacy
parser = spacy.load('en_core_web_lg')

from scipy.sparse import csr_matrix

file_dir = os.path.dirname(__file__)

tweet_directory = os.path.join(file_dir, "../bucket-export/vote-safety-dataflow/tweets/")
output_file = os.path.join(file_dir, "../data/tokenized_tweets_vote_safety.json")

def doc2token(txt, punctuation):

    escape_punct_re = re.compile('[%s]' % re.escape(string.punctuation))
    escape_punct = lambda x: escape_punct_re.sub('', x)


    parsed = parser(txt)
    tokens = list()
    for token in parsed:
        #if token.is_punct or token.is_digit:
        #    continue
        if token.lemma_ in punctuation:
            continue
        #if token.lemma_=='-PRON-':
        #    continue
        else:
            tokens.append(escape_punct(token.lemma_.lower()).strip())
    return tokens



def tokenize(x):

  # preprocess
  
  unescape_html = lambda x: BeautifulSoup(x).get_text().strip()
  remove_urls = lambda x: re.sub("http(.+)?(\W|$)", ' ', x)
  
  normalize_spaces = lambda x: re.sub("[\n\r\t ]+", ' ', x)
  
  remove_leading_mentions = lambda x: re.sub("^(\.?@\w+([^\w]|$))+", '', x)
  #remove_emoji = lambda x: demoji.replace(x, " ")
  
  encodeMention = lambda x: re.sub("@(\w+)", "mention\g<1>", x)
  encodeHashtag = lambda x: re.sub("#(\w+)", "hashtag\g<1>", x)
  
  cleaned_text = encodeHashtag(encodeMention(remove_leading_mentions(normalize_spaces(remove_urls(unescape_html(x)))))) # kept emojis
  
  # remove punctuation 
  
  forbiddens = ['C',
   'k',
   '🇸',
   'c',
   'b',
   't',
   'K',
   'L',
   'Q',
   's',
   'x',
   'F',
   '️',
   'l',
   'j',
   '°',
   'U',
   'J',
   'n',
   'G',
   'A',
   'P',
   'w',
   'E',
   'H',
   'D',
   'R',
   'Y',
   '🇱',
   'f',
   'B',
   'v',
   'e',
   'u',
   'm',
   'r',
   'q',
   '’',
   'O',
   '™',
   'g',
   'p',
   '\u2060',
   'd',
   'V',
   'I',
   'X',
   'h',
   'y',
   'W',
   'S',
   '🇧',
   'o',
   'N',]
  
  punctuation = set(string.punctuation)
  punctuation.update(set(forbiddens))


  tokens = doc2token(cleaned_text, punctuation)
  hashtags = re.findall('#(\w+)', x) 
  return cleaned_text, tokens, hashtags 

  

now = time.time()
for filename in os.listdir(tweet_directory):
  print(filename)
  processed = 0
  with open(os.path.join(tweet_directory, filename), "r") as r:
    for line in r:
      raw= json.loads(line)
      raw = raw['properties']
      data = {} 
      for k, v in raw.items():
        data[k] = compile(v) 
      cleaned_text, tokens, hashtags = tokenize(data['text'])
      data['cleaned_text'] = cleaned_text
      data['tokens'] = tokens
      data['hashtags'] = hashtags
      with open(output_file, "a") as w:
        w.write(json.dumps(data) + "\n")
      processed += 1
      if processed % 10000 == 0:
        print("{} in {} processed: {} sec.".format(processed, filename, time.time() - now))
        now = time.time()
