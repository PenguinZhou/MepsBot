#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS

import numpy as np
import random
import time
import csv
from util import *
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')
from sklearn import svm
import nltk
from joblib import dump, load
from nltk.tokenize import sent_tokenize
from sklearn.ensemble import RandomForestClassifier
from nltk.tokenize import TweetTokenizer
import sys, os, re
lex = liwc.parse_liwc("2015")

def get_vector(doc, cats):
    dic = extract(lex, doc)
    vec = np.zeros(len(cats))
    for i in range(len(cats)):
        if cats[i] in dic.keys():
            vec[i] = dic[cats[i]]
# # Feature of url, show no improvement
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', doc)
    if len(url) > 0:
        vec = np.append(vec, [1])
    else:
        vec = np.append(vec, [0])
# Feature of sentence count, weithed by 10 currently
    sentences = sent_tokenize(doc)
    number_of_sentences = len(sentences)
    if number_of_sentences > 10:
        vec = np.append(vec, [1])
    else:
        sentence_rate = number_of_sentences / 10
        vec = np.append(vec, [sentence_rate])      
# Feature of words count, using twitter curpons, weighted by 100 currently
    tknzr = TweetTokenizer()
    words = tknzr.tokenize(doc)
    number_of_words = len(words)
    if number_of_words > 60:
        vec = np.append(vec, [1])
    else:
        word_rate = number_of_words / 60
        vec = np.append(vec, [word_rate])
    return vec, dic

LIWC_features = ['function', 'pronoun', 'ppron', 'i', 'we', 'you', 'shehe', 'they', 
'ipron', 'article', 'prep', 'auxverb', 'adverb', 'conj', 'negate', 'verb', 'adj', 
'compare', 'interrog', 'number', 'quant', 'affect', 'posemo', 'negemo', 'anger', 
'sad', 'social', 'friend', 'female', 'male', 'cogproc', 'insight', 'cause', 
'discrep', 'tentat', 'certain', 'differ', 'percept', 'see', 'hear', 'feel', 
'bio', 'body', 'health', 'sexual', 'ingest', 'drives', 'affiliation', 'achieve', 
'power', 'reward', 'risk', 'focuspast', 'focuspresent', 'focusfuture', 'relativ', 
'motion', 'space', 'time', 'work', 'leisure', 'home', 'informal', 'swear', 'filler']

IS_clf = load('models/IS_model_all.joblib') 
ES_clf = load('models/ES_model_all.joblib') 

feedback_scripts = ['Everything has two sides and let’s try to see things in a positive light',
					'Write more about it and then free your mind']

app = Flask(__name__, static_url_path='')
CORS(app)
app._static_folder = "static"


experiment_record = []

@app.route('/', methods = ["GET", "POST"])
def index():
	# print(request)
	
	data = list(request.form.to_dict().keys())
	print(data)
	ori_com = data[0]

	if data[0][0:10] == 'Yeah final':
		ori_com = data[0][10:-1]
	click_time = time.time()
	print("Input comment: {}".format(ori_com))
	
	features, details = get_vector(ori_com, LIWC_features)
	IS_score = IS_clf.predict(features.reshape(1, -1))
	ES_score = ES_clf.predict(features.reshape(1, -1))

	# print(details)
	# Logic for the feedback
	ind = random.randint(0, len(feedback_scripts) - 1)
	
	encouragement = feedback_scripts[ind]
	one_record = {'timestamp': click_time, 'input_comment': ori_com, 'IS_score': int(IS_score), 'ES_score': int(ES_score), 'feedback': encouragement,
					'details': str(details)}
	experiment_record.append(one_record)
	print('It takes {} s'.format(time.time() - click_time))
	if data[0][0:10] == 'Yeah final':
		saveFile(data[0][0:10])
		print('Something wrong in this case?')
		return jsonify({'mode': 'AF', 'IS_score': int(IS_score), 'ES_score': int(ES_score), 'feedback': encouragement, 'details': details})
	else:
		return jsonify({'mode': 'AF', 'IS_score': int(IS_score), 'ES_score': int(ES_score), 'feedback': encouragement, 'details': details})

	

# def assess(comment):
# 	features = get_vector(txt, LIWC_features)
#     # print(features)
#     # print(len(features))
#     # print('+' * 40)
#     # print(txt)
#     IS_score = IS_clf.predict(features.reshape(1, -1))
#     ES_score = ES_clf.predict(features.reshape(1, -1))


	# return [IS_score, ES_score, feedback]

def saveFile(comment):
	file_name = 'record/AF_record_' + str(int(time.time())) + '.csv'
	with open(file_name, mode='w', encoding = 'utf_8_sig') as one_task:
		fieldnames = ['index', 'timestamp', 'input_comment', 'IS_score', 'ES_score', 'details', 'feedback']
		csv_writer = csv.DictWriter(one_task, fieldnames=fieldnames)
		csv_writer.writeheader()
		count = 0   
		for i in experiment_record:
			csv.writer(one_task, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow({'index': count, 'timestamp': i['timestamp'], 'input_comment': i['input_comment'], 
								'IS_score': i['IS_score'], 'ES_score': i['ES_score'], 'details': i['details'], 'feedback': i['feedback']})
			count += 1
	# submit_scirpt = 'success'
	# return submit_scirpt
		
if __name__ == '__main__':
	app.run(debug=True)