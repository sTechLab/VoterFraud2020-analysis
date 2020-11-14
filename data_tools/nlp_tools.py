from bs4 import BeautifulSoup
import re
import spacy
import string

parser = spacy.load('en_core_web_lg')


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

def tokenize_tweet(x):
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