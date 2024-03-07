import string
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
import spacy

stopwords_nl = set(stopwords.words('dutch'))
nlp = spacy.load("nl_core_news_sm")

def removepunc(input):
	fixed = []
	for word in input:
		fixed.append(word.translate(str.maketrans('', '', string.punctuation)))
	return fixed

def bigramify(input):
  bi = []
  for index, word in enumerate(input):
  	if index < len(input)-1:
  		if word != '.' and input[index+1] != '.' and '.' not in word:
  			bi.append(word + ' ' + input[index+1])
  return bi

def removestop(input):
	nostops = []
	for word in input:
		if word not in stopwords_nl:
			nostops.append(word)
	return nostops

def lemmatize(splitted):
	lemmatized = []
	for word in splitted:
		add = ''
		doc = nlp(word)
		for token in doc:
			add += token.lemma_
		lemmatized.append(add)
	return lemmatized

unigrams = []
lemma_unigrams = []
lemma_unigrams_stopwords = []

bigrams = []
lemma_bigrams = []
lemma_bigrams_stopwords = []

test =[]
XMLfiles = ["VP_1986.party-topicnr-content.xml",
            "VP_1994.party-topicnr-content.xml",
            "VP_1998.party-topicnr-content.xml"]
for XMLfile in XMLfiles:
  tree = ET.parse(XMLfile)
  year = tree.getroot()
  for party in year:
    for topic in party:
      print(year.attrib['year'] + ' ' + party.attrib['party'] + ' ' + topic.attrib['id'])
      for themes in topic:
      	unigrams.append(themes.tail.translate(str.maketrans('', '', string.punctuation)).split())

      	splitted = themes.tail.split()

      	lemma_unigrams.append(lemmatize(removepunc(splitted)))
      	lemma_unigrams_stopwords.append(lemmatize(removestop(removepunc(splitted))))
       
      	bigrams.append(removepunc(bigramify(splitted)))
      	lemma_bigrams.append(removepunc(bigramify(lemmatize(splitted))))
      	lemma_bigrams_stopwords.append(removepunc(bigramify(lemmatize(removestop(splitted)))))


with open('unigrams.txt', 'w') as f:
	f.write(str(unigrams))

with open('lemma_unigrams.txt', 'w') as f:
	f.write(str(lemma_unigrams))

with open('lemma_unigrams_stopwords.txt', 'w') as f:
	f.write(str(lemma_unigrams_stopwords))
 
with open('bigrams.txt', 'w') as f:
  f.write(str(bigrams))

with open('lemma_bigrams.txt', 'w') as f:
  f.write(str(lemma_bigrams))

with open('lemma_bigrams_stopwords.txt', 'w') as f:
  f.write(str(lemma_bigrams_stopwords))

