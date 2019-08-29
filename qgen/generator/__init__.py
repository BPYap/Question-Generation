import nltk

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download('wordnet')
