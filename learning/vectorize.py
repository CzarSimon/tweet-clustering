from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import re

_stemmer = PorterStemmer()

def remove_url(text):
    text_without_url = re.sub(r"http\S+", "", text)
    return text_without_url

def _tokenize(text):
    return map(lambda term: _stemmer.stem(term), word_tokenize(text))

def vectorize_tweets(tweets):
    vectors = TfidfVectorizer(tokenizer=_tokenize, stop_words='english').fit_transform(tweets)
    return vectors.toarray()
