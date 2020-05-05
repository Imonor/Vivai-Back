# -*- coding: utf-8 -*-

import spacy
from joblib import dump,load
from flask import Flask, json, request
import re

api = Flask(__name__)

@api.route('/', methods=['GET'])
def get_intention():
  if 'q' in request.args:
     query = request.args.get('q')
     intention = getIntention(query)
     return json.dumps([{"response": "success", "results": intention, "plant": "basilic"}])
  else:
     return json.dumps([{"response": "error"}])

def getIntention(sentence):
    
    #load trained model
    clf_svm = load('clf_svm.joblib')
    
    # Pre-processing
    sentence = sentence.lower()
    tokens = nlp_fr(sentence)

    words = []
    allowed_pos = ['VERB', 'NOUN', 'PROPN', 'ADJ']
    vectorizer = load('vectorizer.joblib')
                
    # Lemmatize
    for token in tokens:
        if ( allowed_pos.count(token.pos_) > 0 ):
            if (token.lemma_ != 'plante' and token.lemma_ != 't'): 
                words.append(str(token.lemma_))          
            j = 0;
            vector = vectorizer.get_feature_names()

    # Create vector
    for word in vector:
        vector[j] = words.count(word);           
        j += 1


    p = clf_svm.predict([vector])
    
    intentions = load('intentions.joblib')
	
    score = clf_svm.predict_proba([vector])
    intention_score = score[0][int(p[0])]

    return [intentions[int(p[0])], intention_score]

def identifyWantedPlant(plant_list, sentence):
    # plant_list composed of the species and nicknames of the possessed plants
    sentence = sentence.lower() 
    
    for count,name in enumerate(plant_list):
        if re.findall(name.lower(), sentence):
            # if found, returns the position in the given list
            print("PLANT_NAME="+name)
            return
    return

if __name__ == "__main__":
   nlp_fr = spacy.load('fr_core_news_sm') 
   api.run(host='0.0.0.0', port=5000)
