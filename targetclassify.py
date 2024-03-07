import xml.etree.ElementTree as ET
import ast
import time
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import multilabel_confusion_matrix, classification_report
import numpy as np


XMLfiles = ["Manifestos/VP_1986.party-topicnr-content.xml",
            "Manifestos/VP_1994.party-topicnr-content.xml",
            "Manifestos/VP_1998.party-topicnr-content.xml"]


def get_targets():
  targets = []
  for XMLfile in XMLfiles:
    tree = ET.parse(XMLfile)
    year = tree.getroot()
    for party in year:
      for topic in party:
        for themes in topic:
          new_themes = []
          for theme in themes:
            new_themes.append(theme.attrib['id'])
          targets.append(new_themes)
  return targets


vectorizer = CountVectorizer(analyzer=lambda x: x)
    
themes = get_targets()
targets = vectorizer.fit_transform(themes).toarray()

for prediction in targets:
  if set(prediction) != {0,1} and set(prediction) != {1,0}:
    for index, count in enumerate(prediction):
      if count > 1:
        prediction[index] = 1

#for prediction in targets:
#  if set(prediction) != {0,1}:
#    print(prediction, 'wtf')
#  if set(prediction) != {1,0}:
#    print(prediction, 'wtf2')

with open('data/unigrams.txt', 'r') as f:
  unigrams = ast.literal_eval(f.read())

with open('data/lemma_unigrams.txt', 'r') as f:
  lemma_unigrams = ast.literal_eval(f.read())

with open('data/lemma_unigrams_stopwords.txt', 'r') as f:
  lemma_unigrams_stopwords = ast.literal_eval(f.read())

with open('data/bigrams.txt', 'r') as f:
  bigrams = ast.literal_eval(f.read())

with open('data/lemma_bigrams.txt', 'r') as f:
  lemma_bigrams = ast.literal_eval(f.read())

with open('data/lemma_bigrams_stopwords.txt', 'r') as f:
  lemma_bigrams_stopwords = ast.literal_eval(f.read())


unigramX = vectorizer.fit_transform(unigrams).toarray()
lemma_unigramX = vectorizer.fit_transform(lemma_unigrams).toarray()
lemma_unigrams_stopwordsX = vectorizer.fit_transform(lemma_unigrams_stopwords).toarray()

unibi = []
for uni, bi in zip(unigrams, bigrams):
  unibi.append(uni + bi)
unibiX = vectorizer.fit_transform(unibi).toarray()

lemma_unibi = []
for uni, bi in zip(lemma_unigrams, lemma_bigrams):
  lemma_unibi.append(uni + bi)
lemma_unibiX = vectorizer.fit_transform(lemma_unibi).toarray()

lemma_unibi_stopwords = []
for uni, bi in zip(lemma_unigrams_stopwords, lemma_bigrams_stopwords):
  lemma_unibi_stopwords.append(uni + bi)
lemma_unibi_stopwordsX = vectorizer.fit_transform(lemma_unibi_stopwords).toarray()

names = ['unigramX', 'lemma_unigramX', 'lemma_unigrams_stopwordsX', 'unibiX', 'lemma_unibiX', 'lemma_unibi_stopwordsX']
representations = [unigramX, lemma_unigramX, lemma_unigrams_stopwordsX, unibiX, lemma_unibiX, lemma_unibi_stopwordsX]
start = time.time()
for rep, name in zip(representations, names):
  print(name)
  mid = time.time()
  clf = RandomForestClassifier()
  clf.fit(rep, targets)
  print(classification_report(targets, clf.predict(rep), digits=3))
  print(clf.score(rep, targets))
  print('Time:', time.time()-mid)
  print("============")

print('Total time:', time.time()-start)
print('\a')

