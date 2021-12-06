import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from lxml import etree
from collections import Counter

stopwords = stopwords.words('english')
punctuations = list(string.punctuation)
lemmatizer = WordNetLemmatizer()
xml_file = "news.xml"
dataset = list()
header = list()
root = etree.parse(xml_file).getroot()
corpus = root[0]
for news in corpus:
    header.append(news[0].text)
    news = news[1].text
    tokens = nltk.tokenize.word_tokenize(news.lower())
    lemmas = [lemmatizer.lemmatize(word) for word in tokens]
    lemma_sw = [word for word in lemmas if not word in punctuations]
    lemma_sw_punct = [word for word in lemma_sw if not word in stopwords]
    tokens_lemma_nn = []
    for word in lemma_sw_punct:
        words_lemma = nltk.pos_tag([word])
        for k, v in words_lemma:
            if v == 'NN':
                tokens_lemma_nn.append(k)


    dataset.append(' '.join(i for i in tokens_lemma_nn))

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(dataset)
terms = vectorizer.get_feature_names()
for i in range(len(header)):
    print(header[i] + ':')
    df = pd.DataFrame(tfidf_matrix[i].toarray())
    df = df.transpose().sort_values(by=0, ascending=False).reset_index()
    string_to_print = {}
    for ii in range(10):
        part = terms[int(df.iloc[ii]['index'])]
        string_to_print[part] = df.iloc[ii][0]
    most_common = (sorted(string_to_print.items(), key=lambda t: (t[1], t[0]), reverse=True))
    most_5_word=[]
    for k, v in most_common[:5]:
        most_5_word.append(k)
    print(' '.join(i for i in most_5_word)+'\n')
