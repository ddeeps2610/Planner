import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def lemmatize(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]


def filterStopWords(lems):
    """ 
    Removes the stop words from the list of lems sent and returns list of 
    filtered lems.
    """
    if lems != None:
      return [term for term in lems if term not in stopwords.words('english')]
    return None

