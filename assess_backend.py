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

give_1 = ['Here are my small suggestions:', 'Let me give you some small suggestions:']
give_2 = ['Great! There is one point I think you could improve:', 'Nice! Maybe you would like to try:', 'Good! One small tip:', 'Good job! I have one suggestion that could help you:', 'Well done! I think you could further improve the comment like:']
give_3 = ['Excellent! You can polish the comment if you want:', 'Really supportive! Here is a small tip:', 'Amazing comment! Something you could further improve:']
more_detail = ['How about writing a little bit more detail?', 'You can share more details.', 'Try write down more stuffs.']
more_connect = ['Try support the help seeker using words like:', 'Show connections to the help seeker, using words like:']
pnouns_1 = ["I", "I would", "I will", "I'm", "I have", "I would have", "I mean", "I might", "I think", "me", "myself", "my", "our", "ourselves", "us", "we", "we will", "we have" ]	

pnouns_2 = ["I love you", "thank you", "u", 'ur', 'you are', 'you will', 'you would', 'you have', 'yourself', 'your', 'yours']
pnouns_3 = ['he will', 'he is', 'she will', 'she would', 'her', 'his', 'him', 'himself', 'their', 'them', 'themselves', 'they', 'they will', 'they have', 'they are']
pnouns_4 = ['others', 'it', 'itself', 'no body', 'someone', 'something', 'that', 'that is', 'that will', 'this', 'those', 'what', "what's", 'who', 'who will', 'whose']
more_experience = ['Share experience about yourself or others, like:', 'Share knowledge learn from yourself or others, like:']
social_1 = ['uncle', 'son', 'sister', 'brother', 'parent', 'nephew', 'mother', 'father', 'mom', 'marry', 'grandfather', 'grandmother', 'dad', 'family', 'cousin', 'baby', 'aunt']
social_2 = ['beloved', 'friend', 'best friend', 'boyfriend', 'girlfriend', 'buddy', 'classmate', 'colleague', 'contact', 'darling', 'dear', 'dude', 'ex-boyfriend', 'ex-girlfriend', 'guy', 'honney', 'neighbor', 'partner', 'roommate', 'sweetie']
more_positive = ['You can try to make it more positive with words like:', 'More positive words can be used in the comment, like:']
positive_1 = ['accept', 'active', 'admire', 'agree', 'appreciate', 'bless', 'care', 'encourage', 'enjoy', 'happy', 'hope', 'please', 'share', 'win', 'wisdom']
positive_2 = ['advantage', 'benefit', 'cheer', 'easy', 'fun', 'good', 'great', 'healthy', 'interest', 'joy', 'pretty', 'super', 'support']
positive_3 = ['amazing', 'awesome', 'beautiful', 'best', 'bright', 'comfortable', 'cool', 'exciting', 'excellent', 'fantasy', 'favor', 'helpful', 'honest', 'important', 'inspire', 'nice', 'peace', 'thankful', 'thanks', 'thx', 'useful', 'value', 'warm', 'well', 'welcome', 'wonderful', 'worthwhile']
positive_4 = ['bold', 'brave', 'calm', 'certain', 'clever', 'confident', 'haha', 'hero', 'laugh', 'like', 'lucky', 'perfect', 'positive', 'proud', 'safe', 'smart', 'strong', 'success', 'trust']	


app = Flask(__name__, static_url_path='')
CORS(app)
app._static_folder = "static"

first_click = True

experiment_record = []

@app.route('/', methods = ["GET", "POST"])
def index():
	# print(request)
	# global first_click
	# if first_click:
	# 	experiment_record[:] = []
	data = list(request.form.to_dict().keys())
	print(data)
	ori_com = data[0]
	click_index = data[0].find('click event')
	ori_com = data[0][0:click_index]

	if data[0][0:10] == 'Yeah final':
		click_index = data[0].find('click event')
		ori_com = data[0][10:click_index]
		# ori_com = 
	click_time = time.time()
	print("Input comment: {}".format(ori_com))
	
	features, details = get_vector(ori_com, LIWC_features)
	IS_score = IS_clf.predict(features.reshape(1, -1))
	ES_score = ES_clf.predict(features.reshape(1, -1))

	# Logic for the feedback
	ran_pn1 = random.sample(range(len(pnouns_1)), 3)
	ran_pn2 = random.sample(range(len(pnouns_2)), 3)
	ran_pn3 = random.sample(range(len(pnouns_3)), 3)
	ran_pn4 = random.sample(range(len(pnouns_4)), 3)
	ran_so1 = random.sample(range(len(social_1)), 6)
	ran_so2 = random.sample(range(len(social_2)), 6)
	ran_po1 = random.sample(range(len(positive_1)), 3)
	ran_po2 = random.sample(range(len(positive_2)), 3)
	ran_po3 = random.sample(range(len(positive_3)), 3)
	ran_po4 = random.sample(range(len(positive_4)), 3)
	feedback_1 = ''
	feedback_2 = ''
	score_pnouns = 0
	score_social = 0
	score_positive = 0
	if 'ppron' in details.keys():
		score_pnouns = details['ppron']
	if 'social' in details.keys():
		score_social = details['social']
	if 'posemo' in details.keys():
		score_positive = details['posemo']

	


	if IS_score < 3 and ES_score < 3:
		ran_0 = random.randint(0, 1)
		feedback_1 = give_1[random.randint(0, len(give_1) - 1)]
		if ran_0 == 0:
			ran = random.randint(0, 2)
			if ran == 0: #score_pnouns == min(score_pnouns, score_positive, score_social) and random.randint(0, 1) == 1:
				feedback_2 = more_connect[random.randint(0, len(more_connect) - 1)] + '<br>' + '<br>' + pnouns_1[ran_pn1[0]] + ', ' + pnouns_1[ran_pn1[1]] + ', ' + pnouns_1[ran_pn1[2]] + ', ' + pnouns_2[ran_pn2[0]] + ', ' + pnouns_2[ran_pn2[1]] + ', ' + pnouns_2[ran_pn2[2]] + ', ' + pnouns_3[ran_pn3[0]] + ', ' + pnouns_3[ran_pn3[1]] + ', '  + pnouns_3[ran_pn3[2]] + ', ' + pnouns_4[ran_pn4[0]] + ', ' + pnouns_4[ran_pn4[1]] + ', ' + pnouns_4[ran_pn4[2]] + '.'
			elif ran == 1: #score_social == min(score_pnouns, score_positive, score_social) and random.randint(0, 1) == 1:
				feedback_2 = more_experience[random.randint(0, len(more_experience) - 1)] + '<br>'+ '<br>'  + social_1[ran_so1[0]] + ', ' + social_1[ran_so1[1]] + ', ' + social_1[ran_so1[2]] + ', ' + social_1[ran_so1[3]] + ', ' + social_2[ran_so2[0]] + ', ' + social_2[ran_so2[1]] + ', ' + social_2[ran_so2[2]] +  ', ' + social_2[ran_so2[3]]  + '.'
			else: # : score_positive == min(score_pnouns, score_positive, score_social)
				feedback_2 = more_positive[random.randint(0, len(more_positive) - 1)] + '<br>'+ '<br>'  + positive_1[ran_po1[0]] + ', ' + positive_1[ran_po1[1]] + ', ' + positive_1[ran_po1[2]] + ', ' + positive_2[ran_po2[0]] + ', ' + positive_2[ran_po2[1]] + ', ' + positive_2[ran_po2[2]] + ', ' + positive_3[ran_po3[0]] + ', ' + positive_3[ran_po3[1]] + ', '  + positive_3[ran_po3[2]] + ', ' + positive_4[ran_po4[0]] + ', ' + positive_4[ran_po4[1]] + ', ' + positive_4[ran_po4[2]] + '.'
		else:
			if score_pnouns == min(score_pnouns, score_positive, score_social):
				feedback_2 = more_connect[random.randint(0, len(more_connect) - 1)] + '<br>' + '<br>' + pnouns_1[ran_pn1[0]] + ', ' + pnouns_1[ran_pn1[1]] + ', ' + pnouns_1[ran_pn1[2]] + ', ' + pnouns_2[ran_pn2[0]] + ', ' + pnouns_2[ran_pn2[1]] + ', ' + pnouns_2[ran_pn2[2]] + ', ' + pnouns_3[ran_pn3[0]] + ', ' + pnouns_3[ran_pn3[1]] + ', '  + pnouns_3[ran_pn3[2]] + ', ' + pnouns_4[ran_pn4[0]] + ', ' + pnouns_4[ran_pn4[1]] + ', ' + pnouns_4[ran_pn4[2]] + '.'
			elif score_social == min(score_pnouns, score_positive, score_social):
				feedback_2 = more_experience[random.randint(0, len(more_experience) - 1)] + '<br>'+ '<br>'  + social_1[ran_so1[0]] + ', ' + social_1[ran_so1[1]] + ', ' + social_1[ran_so1[2]] + ', ' + social_1[ran_so1[3]] + ', ' + social_2[ran_so2[0]] + ', ' + social_2[ran_so2[1]] + ', ' + social_2[ran_so2[2]] +  ', ' + social_2[ran_so2[3]]  + '.'
			else: # : score_positive == min(score_pnouns, score_positive, score_social)
				feedback_2 = more_positive[random.randint(0, len(more_positive) - 1)] + '<br>'+ '<br>'  + positive_1[ran_po1[0]] + ', ' + positive_1[ran_po1[1]] + ', ' + positive_1[ran_po1[2]] + ', ' + positive_2[ran_po2[0]] + ', ' + positive_2[ran_po2[1]] + ', ' + positive_2[ran_po2[2]] + ', ' + positive_3[ran_po3[0]] + ', ' + positive_3[ran_po3[1]] + ', '  + positive_3[ran_po3[2]] + ', ' + positive_4[ran_po4[0]] + ', ' + positive_4[ran_po4[1]] + ', ' + positive_4[ran_po4[2]] + '.'
		

	elif IS_score == 3 and ES_score == 3:
		ran_0 = random.randint(0, 1)
		feedback_1 = give_3[random.randint(0, len(give_3) - 1)]
		if ran_0 == 0:
			ran = random.randint(0, 2)
			if ran == 0: #score_pnouns == min(score_pnouns, score_positive, score_social) and random.randint(0, 1) == 1:
				feedback_2 = more_connect[random.randint(0, len(more_connect) - 1)] + '<br>' + '<br>' + pnouns_1[ran_pn1[0]] + ', ' + pnouns_1[ran_pn1[1]] + ', ' + pnouns_1[ran_pn1[2]] + ', ' + pnouns_2[ran_pn2[0]] + ', ' + pnouns_2[ran_pn2[1]] + ', ' + pnouns_2[ran_pn2[2]] + ', ' + pnouns_3[ran_pn3[0]] + ', ' + pnouns_3[ran_pn3[1]] + ', '  + pnouns_3[ran_pn3[2]] + ', ' + pnouns_4[ran_pn4[0]] + ', ' + pnouns_4[ran_pn4[1]] + ', ' + pnouns_4[ran_pn4[2]] + '.'
			elif ran == 1: #score_social == min(score_pnouns, score_positive, score_social) and random.randint(0, 1) == 1:
				feedback_2 = more_experience[random.randint(0, len(more_experience) - 1)] + '<br>'+ '<br>'  + social_1[ran_so1[0]] + ', ' + social_1[ran_so1[1]] + ', ' + social_1[ran_so1[2]] + ', ' + social_1[ran_so1[3]] + ', ' + social_2[ran_so2[0]] + ', ' + social_2[ran_so2[1]] + ', ' + social_2[ran_so2[2]] +  ', ' + social_2[ran_so2[3]]  + '.'
			else: # : score_positive == min(score_pnouns, score_positive, score_social)
				feedback_2 = more_positive[random.randint(0, len(more_positive) - 1)] + '<br>'+ '<br>'  + positive_1[ran_po1[0]] + ', ' + positive_1[ran_po1[1]] + ', ' + positive_1[ran_po1[2]] + ', ' + positive_2[ran_po2[0]] + ', ' + positive_2[ran_po2[1]] + ', ' + positive_2[ran_po2[2]] + ', ' + positive_3[ran_po3[0]] + ', ' + positive_3[ran_po3[1]] + ', '  + positive_3[ran_po3[2]] + ', ' + positive_4[ran_po4[0]] + ', ' + positive_4[ran_po4[1]] + ', ' + positive_4[ran_po4[2]] + '.'
		else:
			if score_pnouns == min(score_pnouns, score_positive, score_social):
				feedback_2 = more_connect[random.randint(0, len(more_connect) - 1)] + '<br>' + '<br>' + pnouns_1[ran_pn1[0]] + ', ' + pnouns_1[ran_pn1[1]] + ', ' + pnouns_1[ran_pn1[2]] + ', ' + pnouns_2[ran_pn2[0]] + ', ' + pnouns_2[ran_pn2[1]] + ', ' + pnouns_2[ran_pn2[2]] + ', ' + pnouns_3[ran_pn3[0]] + ', ' + pnouns_3[ran_pn3[1]] + ', '  + pnouns_3[ran_pn3[2]] + ', ' + pnouns_4[ran_pn4[0]] + ', ' + pnouns_4[ran_pn4[1]] + ', ' + pnouns_4[ran_pn4[2]] + '.'
			elif score_social == min(score_pnouns, score_positive, score_social):
				feedback_2 = more_experience[random.randint(0, len(more_experience) - 1)] + '<br>'+ '<br>'  + social_1[ran_so1[0]] + ', ' + social_1[ran_so1[1]] + ', ' + social_1[ran_so1[2]] + ', ' + social_1[ran_so1[3]] + ', ' + social_2[ran_so2[0]] + ', ' + social_2[ran_so2[1]] + ', ' + social_2[ran_so2[2]] +  ', ' + social_2[ran_so2[3]]  + '.'
			else: # : score_positive == min(score_pnouns, score_positive, score_social)
				feedback_2 = more_positive[random.randint(0, len(more_positive) - 1)] + '<br>'+ '<br>'  + positive_1[ran_po1[0]] + ', ' + positive_1[ran_po1[1]] + ', ' + positive_1[ran_po1[2]] + ', ' + positive_2[ran_po2[0]] + ', ' + positive_2[ran_po2[1]] + ', ' + positive_2[ran_po2[2]] + ', ' + positive_3[ran_po3[0]] + ', ' + positive_3[ran_po3[1]] + ', '  + positive_3[ran_po3[2]] + ', ' + positive_4[ran_po4[0]] + ', ' + positive_4[ran_po4[1]] + ', ' + positive_4[ran_po4[2]] + '.'
		
		
	else:
		ran_0 = random.randint(0, 1)
		print(ran_0)
		feedback_1 = give_2[random.randint(0, len(give_2) - 1)]
		if ran_0 == 0:
			ran = random.randint(0, 1)
			print(1)
			if IS_score == 3:
				if ran == 0: #score_pnouns == min(score_pnouns, score_positive, score_social):
					print(2)
					feedback_2 = more_connect[random.randint(0, len(more_connect) - 1)] + '<br>'+ '<br>'  + pnouns_1[ran_pn1[0]] + ', ' + pnouns_1[ran_pn1[1]] + ', ' + pnouns_1[ran_pn1[2]] + ', ' + pnouns_2[ran_pn2[0]] + ', ' + pnouns_2[ran_pn2[1]] + ', ' + pnouns_2[ran_pn2[2]] + ', ' + pnouns_3[ran_pn3[0]] + ', ' + pnouns_3[ran_pn3[1]] + ', '  + pnouns_3[ran_pn3[2]] + ', ' + pnouns_4[ran_pn4[0]] + ', ' + pnouns_4[ran_pn4[1]] + ', ' + pnouns_4[ran_pn4[2]] + '.'
				if ran == 1: #score_social == min(score_pnouns, score_positive, score_social):
					feedback_2 = more_positive[random.randint(0, len(more_positive) - 1)] + '<br>'+ '<br>'  + social_1[ran_so1[0]] + ', ' + social_1[ran_so1[1]] + ', ' + social_1[ran_so1[2]] + ', ' + social_1[ran_so1[3]] + ', ' + social_2[ran_so2[0]] + ', ' + social_2[ran_so2[1]] + ', ' + social_2[ran_so2[2]] +  ', ' + social_2[ran_so2[3]]  + '.'
			else:	
				if ran==0: #score_positive == min(score_pnouns, score_positive, score_social):
					feedback_2 = more_positive[random.randint(0, len(more_positive) - 1)] + '<br>'+ '<br>'  + positive_1[ran_po1[0]] + ', ' + positive_1[ran_po1[1]] + ', ' + positive_1[ran_po1[2]] + ', ' + positive_2[ran_po2[0]] + ', ' + positive_2[ran_po2[1]] + ', ' + positive_2[ran_po2[2]] + ', ' + positive_3[ran_po3[0]] + ', ' + positive_3[ran_po3[1]] + ', '  + positive_3[ran_po3[2]] + ', ' + positive_4[ran_po4[0]] + ', ' + positive_4[ran_po4[1]] + ', ' + positive_4[ran_po4[2]] + '.'
				if ran==1: #score_social == min(score_pnouns, score_positive, score_social):
					feedback_2 = more_experience[random.randint(0, len(more_experience) - 1)] + '<br>'+ '<br>'  + social_1[ran_so1[0]] + ', ' + social_1[ran_so1[1]] + ', ' + social_1[ran_so1[2]] + ', ' + social_1[ran_so1[3]] + ', ' + social_2[ran_so2[0]] + ', ' + social_2[ran_so2[1]] + ', ' + social_2[ran_so2[2]] +  ', ' + social_2[ran_so2[3]]  + '.'
		else:
			if IS_score == 3:
				if score_pnouns == min(score_pnouns, score_positive, score_social):
					feedback_2 = more_connect[random.randint(0, len(more_connect) - 1)] + '<br>'+ '<br>'  + pnouns_1[ran_pn1[0]] + ', ' + pnouns_1[ran_pn1[1]] + ', ' + pnouns_1[ran_pn1[2]] + ', ' + pnouns_2[ran_pn2[0]] + ', ' + pnouns_2[ran_pn2[1]] + ', ' + pnouns_2[ran_pn2[2]] + ', ' + pnouns_3[ran_pn3[0]] + ', ' + pnouns_3[ran_pn3[1]] + ', '  + pnouns_3[ran_pn3[2]] + ', ' + pnouns_4[ran_pn4[0]] + ', ' + pnouns_4[ran_pn4[1]] + ', ' + pnouns_4[ran_pn4[2]] + '.'
				else: #if score_social == min(score_pnouns, score_positive, score_social):
					feedback_2 = more_positive[random.randint(0, len(more_positive) - 1)] + '<br>'+ '<br>'  + social_1[ran_so1[0]] + ', ' + social_1[ran_so1[1]] + ', ' + social_1[ran_so1[2]] + ', ' + social_1[ran_so1[3]] + ', ' + social_2[ran_so2[0]] + ', ' + social_2[ran_so2[1]] + ', ' + social_2[ran_so2[2]] +  ', ' + social_2[ran_so2[3]]  + '.'
			else:	
				if score_positive == min(score_pnouns, score_positive, score_social):
					feedback_2 = more_positive[random.randint(0, len(more_positive) - 1)] + '<br>'+ '<br>'  + positive_1[ran_po1[0]] + ', ' + positive_1[ran_po1[1]] + ', ' + positive_1[ran_po1[2]] + ', ' + positive_2[ran_po2[0]] + ', ' + positive_2[ran_po2[1]] + ', ' + positive_2[ran_po2[2]] + ', ' + positive_3[ran_po3[0]] + ', ' + positive_3[ran_po3[1]] + ', '  + positive_3[ran_po3[2]] + ', ' + positive_4[ran_po4[0]] + ', ' + positive_4[ran_po4[1]] + ', ' + positive_4[ran_po4[2]] + '.'
				else: # score_social == min(score_pnouns, score_positive, score_social):
					feedback_2 = more_experience[random.randint(0, len(more_experience) - 1)] + '<br>'+ '<br>'  + social_1[ran_so1[0]] + ', ' + social_1[ran_so1[1]] + ', ' + social_1[ran_so1[2]] + ', ' + social_1[ran_so1[3]] + ', ' + social_2[ran_so2[0]] + ', ' + social_2[ran_so2[1]] + ', ' + social_2[ran_so2[2]] +  ', ' + social_2[ran_so2[3]]  + '.'
				

	feedback_1_1 = more_detail[random.randint(0, len(more_detail) - 1)]
	tknzr = TweetTokenizer()
	words = tknzr.tokenize(ori_com)
	num_word = len(words)
	global first_click
	if num_word < 60 and first_click:
		feedback_2 = feedback_1_1 + '<br>' + feedback_2
		first_click = False

	one_record = {'timestamp': click_time, 'input_comment': ori_com, 'IS_score': int(IS_score), 'ES_score': int(ES_score), 'feedback_1': feedback_1, 'feedback_2': feedback_2,
					'details': str(details)}
	experiment_record.append(one_record)
	print('It takes {} s'.format(time.time() - click_time))
	if data[0][0:10] == 'Yeah final':
		saveFile(data[0][0:10])
		# print('Something wrong in this case?')
		experiment_record[:] = []
		return jsonify({'mode': 'AF', 'IS_score': int(IS_score), 'ES_score': int(ES_score), 'feedback_1': feedback_1, 'feedback_2': feedback_2, 'details': details})
	else:
		return jsonify({'mode': 'AF', 'IS_score': int(IS_score), 'ES_score': int(ES_score), 'feedback_1': feedback_1, 'feedback_2': feedback_2, 'details': details})

	

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
		fieldnames = ['index', 'timestamp', 'input_comment', 'IS_score', 'ES_score', 'details', 'feedback_1', 'feedback_2']
		csv_writer = csv.DictWriter(one_task, fieldnames=fieldnames)
		csv_writer.writeheader()
		count = 0   
		for i in experiment_record:
			csv.writer(one_task, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow({'index': count, 'timestamp': i['timestamp'], 'input_comment': i['input_comment'], 
								'IS_score': i['IS_score'], 'ES_score': i['ES_score'], 'details': i['details'], 'feedback_1': i['feedback_1'], 'feedback_2': i['feedback_2']})
			count += 1
	# submit_scirpt = 'success'
	global first_click
	first_click = True
	# return submit_scirpt
		
if __name__ == '__main__':
	app.run(debug=True)