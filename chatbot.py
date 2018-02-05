import numpy as np
import tensorflow as tf
import re
import time
import codecs
import warnings
import io


#import the dataset
lines = io.open('movie_lines.txt',encoding='utf-8',errors='ignore').read().split('\n')
conversation=io.open('movie_conversations.txt',encoding='utf-8',errors='ignore').read().split('\n')

#create a dictionary that maps each line and its id
id_to_line = {}
for line in lines:
	_line=line.split(' +++$+++ ')
	if len(_line) == 5:
		id_to_line[_line[0]]=_line[4]

#creating a list of all conversations
conv_ids=[]
for conv in conversation[:-1]:
	_conv=conv.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
	conv_ids.append(_conv.split(','))

#Getting ques and answers
ques=[]
ans=[]
for conv  in conv_ids:
	for i in range(0,len(conv)-1):
		ques.append(id_to_line[conv[i]])
		ans.append(id_to_line[conv[i+1]])

#clean texts

def clean_text(text):
	text = text.lower()
	text = re.sub(r"i'm","i am",text)
	text = re.sub(r"he's","he is",text)
	text = re.sub(r"she's","she is",text)
	text = re.sub(r"that's","that is",text)
	text = re.sub(r"what's","what is",text)
	text = re.sub(r"where's","where is",text)
	text = re.sub(r"\'ll"," will",text)
	text = re.sub(r"\'re"," are",text)
	text = re.sub(r"\'ve"," have",text)
	text = re.sub(r"\'d"," would",text)
	text = re.sub(r"\'s"," us",text)
	text = re.sub(r"won't","will not",text)
	text = re.sub(r"can't","cannot",text)
	text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]","",text)
	return text

#cleaning the questions and answers
clean_ques=[]
for qs in ques:
	clean_ques.append(clean_text(qs))

clean_ans=[]
for a in ans:
	clean_ans.append(clean_text(a))

#creating a dictionary that maps each word to its no of occurences
word_to_count ={}
for ques in clean_ques:
	for word in ques.split():
		if word not in word_to_count:
			word_to_count[word]=1
		else:
			word_to_count[word]+=1

for ans in clean_ans:
	for word in ans.split():
		if word not in word_to_count:
			word_to_count[word]=1
		else:
			word_to_count[word]+=1

#creating two dicts that map the ques words and the ans words to a uniq integer
threshold = 20

ques_words_int={}
word_no=0

for word, count in word_to_count.items():
	if count >= threshold:
		ques_words_int[word]=word_no
		word_no+=1
ans_words_int={}
word_no=0
for word, count in word_to_count.items():
	if count >= threshold:
		ans_words_int[word]=word_no
		word_no+=1

#add last tokens to two dictionaries

tokens=['<PAD>','<EOS>','<OUT>','<SOS>']

for token in tokens:
	ques_words_int[token]=len(ques_words_int)+1
	ans_words_int[token]=len(ans_words_int)+1

#creating the inverse dict of the ans_words_int dict
ans_int_words={w_i: w for w, w_i in ans_words_int.items()}

#adding the end of string token to the end of every answer
for i in range(len(clean_ans)):
	clean_ans[i]+=' <EOS>'

#Translating all ques and ans into integers
#replacing all the words that were filtered out by <OUT>

ques_to_int=[]
for ques in clean_ques:
	ints=[]
	for word in ques.split():
		if word not in ques_words_int:
			ints.append(ques_words_int['<OUT>'])
		else:
			ints.append(ques_words_int[word])
	ques_to_int.append(ints)

ans_to_int=[]
for ans in clean_ans:
	ints=[]
	for word in ans.split():
		if word not in ans_words_int:
			ints.append(ans_words_int['<OUT>'])
		else:
			ints.append(ans_words_int['<OUT>'])
	ans_to_int.append(ints)

#sorting ques and ans by length of the ques
sorted_clean_ques=[]
sorted_clean_ans=[]

for length in range(1,26):
	 for i in enumerate(ques_to_int):
		if len(i[1])== length:
			sorted_clean_ques.append(ques_to_int[i[0]])
			sorted_clean_ans.append(ans_to_int[i[0]])
		






















	
