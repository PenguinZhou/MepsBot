#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS


from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections
from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial

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
print('it is running!')

# Leave the LIWC part currently, to see if it is time consuming... It seems that it only takes 0.016s
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

feedback_scripts = ['<b> I found some good comments with highlighted words that could help you reflect: </b>',
					'<b> I found some highly rated examples with parts of interests highlighted: </b>',
					'<b> Here are some relevant good comments for your reference: </b>',
					'<b> You may want to take a look at these highly rated comments: </b>',
					'<b> I got some great relevant comments with highlighted words for you: </b>']



# We create two python files because in the assessment mode, we do not
# need create Elastic and Bert servers; and also, to make it not that complicate..

# Remember to turn on the Elastic search server and Bert server first
# 运行 bin/elasticsearch.bat 启动数据库服务器
# 在BERT model 文件夹运行
# C:\Users\Penguin\AppData\Roaming\Python\Python36\Scripts\bert-serving-start.exe -model_dir uncased_L-12_H-768_A-12\ -num_worker=1 -max_seq_len=128
# 打开BERT server

bc = BertClient()
es = Elasticsearch()
first_click = True
app = Flask(__name__, static_url_path='')
CORS(app)
app._static_folder = "static"

pnouns_1 = ["I would", "I will", "I've", "I'm", "I have", "I would have", "I mean", "I might", "I think", "me", "myself", "my", "our", "ourselves", "us", "we will", "we have", "I", "we"]	
pnouns_2 = ["I love you", "thank you", 'ur', 'you are', 'you will', 'you would', 'you have', 'yourself', 'your', 'yours', 'you', 'u']
pnouns_3 = ['he will', 'he is', 'she will', 'she would', 'himself', 'their', 'them', 'themselves', 'they', 'they will', 'they have', 'they are', 'her', 'his', 'him']
pnouns_4 = ['others', 'itself', 'no body', 'someone', 'something', 'that is', 'that will', 'this', 'those', 'what', "what's", 'who will', 'whose', 'it', 'who', 'that']
# more_experience = ['Share experience about yourself or others, like:', 'Share knowledge learn from yourself or others, like:']
social_1 = ['uncle', 'son', 'sister', 'brother', 'parent', 'nephew', 'mother', 'father', 'mom', 'marry', 'grandfather', 'grandmother', 'dad', 'family', 'cousin', 'baby', 'aunt']
social_2 = ['beloved', 'friends', 'friend', 'best friend', 'boyfriend', 'girlfriend', 'buddy', 'classmate', 'colleague', 'contact', 'darling', 'dear', 'dude', 'ex-boyfriend', 'ex-girlfriend', 'guy', 'honney', 'neighbor', 'partner', 'roommate', 'sweetie']
# more_positive = ['You can try to make it more positive with words like:', 'More positive words can be used in the comment, like:']
positive_1 = ['accepted', 'accept', 'active', 'admire', 'agreed', 'agree', 'appreciate', 'bless', 'care', 'encourage', 'enjoy', 'happy', 'hope', 'please', 'share', 'win', 'wisdom']
positive_2 = ['advantages', 'advantage', 'benefits', 'benefit', 'cheer', 'easy', 'easiest', 'funny', 'fun',  'good', 'great', 'healthy', 'interest', 'joy', 'pretty', 'super', 'support']
positive_3 = ['amazing', 'awesome', 'beautiful', 'better', 'best', 'bright', 'comfortable', 'cool', 'exciting', 'excited', 'excellent', 'fantasy', 'favor', 'helpful', 'honest', 'important', 'inspired', 'inspiring', 'inspire', 'nice', 'peaceful', 'peace', 'thankful', 'thanks', 'thx', 'useful', 'valuable', 'value', 'warm', 'well', 'welcome', 'wonderful', 'worthwhile']
positive_4 = ['bold', 'brave', 'calm', 'certain', 'clever', 'confident', 'haha', 'smile', 'hero', 'laugh', 'like', 'lucky', 'perfect', 'positive', 'pround', 'safe', 'smart', 'strong', 'success', 'trust']	
experiment_record = []
mark_word_list_1 = pnouns_1 + pnouns_2 + pnouns_3 + pnouns_4
mark_word_list_2 = social_1 + social_2 
mark_word_list_3 = positive_1 + positive_2 + positive_3 + positive_4



@app.route('/', methods = ["GET", "POST"])
def index():
	global first_click
	global experiment_record
	if first_click:
		experiment_record = []
		# print(11111111111111111111111111111111111111111111111111111111111)
		first_click = False
	data = list(request.form.to_dict().keys())
	# print(data)
	ori_com = data[0]
	click_index = data[0].find('click event')
	ori_com = data[0][0:click_index]

	if data[0][0:10] == 'Yeah final':
		click_index = data[0].find('click event')
		ori_com = data[0][10:click_index]
		first_click = True
	click_time = time.time()
	print("Input comment: {}".format(ori_com))
	
	features, details = get_vector(ori_com, LIWC_features)
	IS_score = IS_clf.predict(features.reshape(1, -1))
	ES_score = ES_clf.predict(features.reshape(1, -1))


	dsl = {
		'query': {
			'match': {
				'body': ori_com
			}
		}
	}
	search_size = 50
	# ind = random.randint(0, search_size)
	result = es.search(index = 'is_es_3_256', size = search_size, body = dsl)
	result_list = result['hits']['hits']
	vec = bc.encode([ori_com])
	result_cos = []
	for re_1 in result_list:
		sto_vec = np.array(re_1['_source']['bert_vec'])
		cos_sim = cosine_similarity([vec[0],sto_vec])[0][1]
		result_cos.append({'body': re_1['_source']['body'], 'cos_score': cos_sim})
	re_sort = sorted(result_cos, key=lambda s: s['cos_score'], reverse=True)
	feedback = feedback_scripts[random.randint(0, len(feedback_scripts) - 1)] 
	candidates = {'mode': 'RE', 'feedback': feedback, '0': re_sort[0]['body'], '1': re_sort[1]['body'], '2': re_sort[2]['body'], '3': re_sort[3]['body'],
				'4': re_sort[4]['body'], '5': re_sort[5]['body'], '6': re_sort[6]['body'], '7': re_sort[7]['body'], '8': re_sort[8]['body'],
				'9': re_sort[9]['body'], '10': re_sort[10]['body'], '11': re_sort[11]['body'], '12': re_sort[12]['body'], 
				'13': re_sort[13]['body'] ,'14': re_sort[14]['body'], '15': re_sort[15]['body'], '16': re_sort[16]['body'], '17': re_sort[17]['body']
				}
	print('It takes {} s'.format(time.time() - click_time))
	one_record = {'timestamp': click_time, 'input_comment': ori_com, 'IS_score': int(IS_score), 'ES_score': int(ES_score), 'details': details, 'candidates': candidates, 'feedback': feedback, 'click_event': data[0][click_index:-1]}
	experiment_record.append(one_record)
	# print(one_record['candidates']['0'])	

	mark_candidates = {}
	for key in candidates.keys():
		mark_candidates[key] = candidates[key]
	# mark_candidates['1'] = 'hahaha'
	# print(candidates['1'])
	for i in range(0, 18):
		for word in mark_word_list_1:
			# print('1')
			if re.search(r'\b' + word + r'\b', mark_candidates[str(i)], re.IGNORECASE) != None:
				# print('2')
				mark_candidates[str(i)] = re.sub(r'\b' + word + r'\b', '<font color=blue>' + word + '</font>', mark_candidates[str(i)], flags=re.IGNORECASE)
				# print(mark_candidates[str(i)])
		for word in mark_word_list_2:
			if re.search(r'\b' + word + r'\b', mark_candidates[str(i)], re.IGNORECASE) != None:
				# print('2')
				mark_candidates[str(i)] = re.sub(r'\b' + word + r'\b', '<mark><font color=green>' + word + '</font></mark>', mark_candidates[str(i)], flags=re.IGNORECASE)
		for word in mark_word_list_3:
			if re.search(r'\b' + word + r'\b', mark_candidates[str(i)], re.IGNORECASE) != None:
				# print('2')
				mark_candidates[str(i)] = re.sub(r'\b' + word + r'\b', '<mark><font color=red>' + word + '</font></mark>', mark_candidates[str(i)], flags=re.IGNORECASE)
	# print(one_record['candidates']['0'])
	# print(candidates['0'])			
	if data[0][0:10] == 'Yeah final':
		saveFile(data[0][10:-1])
		# print('Something wrong in this case?')
		experiment_record = []
		return jsonify(mark_candidates)
	else:
		return jsonify(mark_candidates)

def saveFile(comment):
	# click_index = comment.find('click event')
	
	file_name = 'record/RE_record_' + str(int(time.time())) + '.csv'
	with open(file_name, mode='w', encoding = 'utf_8_sig') as one_task:
		fieldnames = ['index', 'timestamp', 'input_comment', 'IS_score', 'ES_score', 'details', 'candidates', 'feedback', 'click_event']
		csv_writer = csv.DictWriter(one_task, fieldnames=fieldnames)
		csv_writer.writeheader()
		count = 0   
		
		for i in experiment_record:
			print(i)
			csv.writer(one_task, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow({'index': count, 'timestamp': i['timestamp'], 'input_comment': i['input_comment'], 
								'IS_score': i['IS_score'], 'ES_score': i['ES_score'], 'details': i['details'], 'candidates': i['candidates'], 'feedback': i['feedback'], 'click_event': i['click_event']})
			count += 1
		
	# submit_scirpt = 'success'
	# return submit_scirpt

# def assess(comment):
# 	features = get_vector(txt, LIWC_features)
#     # print(features)
#     # print(len(features))
#     # print('+' * 40)
#     # print(txt)
#     IS_score = IS_clf.predict(features.reshape(1, -1))
#     ES_score = ES_clf.predict(features.reshape(1, -1))


	# return [IS_score, ES_score, feedback]


		
if __name__ == '__main__':
	app.run(debug=True)