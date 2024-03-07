import xml.etree.ElementTree as ET
import ast
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np

def performance(classifier, name, data, target):
	classifier.fit(data, target)
	predicted = classifier.predict(data)
	print("predicted: ",predicted)
'''
	print(name + ' performance:')
	#print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names, zero_division=0))
	new = metrics.classification_report(target, predicted, target_names=twenty_test.target_names, zero_division=0, output_dict=True)['weighted avg']
	print(new)
	print('-=-=-=-=-=-=-=-=-=-=-=-')
	return(new)'''


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
    
themes = get_targets()

with open('data/unigrams.txt', 'r') as f:
  unigrams = ast.literal_eval(f.read())

vectorizer = CountVectorizer(analyzer=lambda x: x)
unigramX = vectorizer.fit_transform(unigrams).toarray()
targets = vectorizer.fit_transform(themes).toarray()


print(unigramX[0])
print(targets[0])

print('X: ', unigramX.shape)
print('Y: ', np.asarray(targets, dtype=object).shape)
  
clf = RandomForestClassifier()
clf.fit(unigramX, targets)
print(clf.score(unigramX, targets))
'''
RFtf = Pipeline([
	('vect', CountVectorizer()),
	('tf', TfidfTransformer(use_idf=False)),
	('clf', RandomForestClassifier(random_state=69)),
])
performance(RFtf, 'Random Forest TF', Xvalues, targets)
'''

