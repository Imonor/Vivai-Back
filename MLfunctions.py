# -*- coding: utf-8 -*-

import spacy
from joblib import load
import re
import unidecode

def getIntention(sentence):
    
    #load trained model
    clf_svm = load('clf_svm.joblib')
    
    # Pre-processing
    sentence = sentence.lower()

    nlp_fr = spacy.load('fr_core_news_sm')
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
    return(intentions[int(p[0])])

def identifyWantedPlant(plant_list, sentence):
    # plant_list composed of the species and nicknames of the possessed plants

    sentence = unidecode.unidecode(sentence.lower())

    for count,name in enumerate(plant_list):
        if re.findall(unidecode.unidecode(name.lower()), sentence):
            # if found, returns the position in the given list
            return count
    return -1
