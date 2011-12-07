#!/usr/bin/env python
# encoding: utf-8
"""
sentiment_analyzer.py

Created by Elvar Orn Unnthorsson on 07-12-2011
Copyright (c) 2011 ellioman inc. All rights reserved.
"""

import sys
import os
from os.path import join as pjoin
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
import codecs
import re

class SentimentAnalyzer:
	
	"""
	SentimentAnalyzer trains a Naive Bayes classifier so that it can determine whether a tweet
	is positive, negative or neutral. It uses training data that was manually categorized by
	the author. The analyze function should be used to classify a list of tweets to analyze.
	"""
	
	def __init__( self ):
		"""
		Constructs a new SentimentAnalyzer instance.
		"""
		
		self.results = { "positive": 0, "negative": 0, "neutral": 0}
		self.data = {}
		self.min_word_length = 3
		
		self.stopSet = set(stopwords.words('english'))
		extra_stopwords = ["he's", "she's", "RT" ]
		for stopword in extra_stopwords: self.stopSet.add( stopword )
		
		# Naive Bayes initialization
		self.__init_naive_bayes()
	
	
	def analyze(self, data):
		"""
		analyze(self, data):
		Input: data. A list of tweets to analyze.
		Takes a list of tweets and uses sentiment analysis to determine whether 
		each tweet is positive, negative or neutral.
		Return: The tweets list with each tweet categorized with the proper sentiment value.
		"""
		
		return self.__analyse_using_naive_bayes( data )
	
	
	def get_analysis_result(self, data_to_get):
		"""
		get_analysis_result(self, data_to_get):
		Input: data_to_get. The statistic that the function should get from the results dictionary.
		Gets the count of either positive, negative or neutral from the results dictionary after 
		doing an analysis. 
		Return: The count of positive, negative or positive tweets found during the analysis.
		"""
		
		return self.results[data_to_get]
	
	
	def show_most_informative_features( self, amount ):
		"""
		show_most_informative_features( self, amount ):
		Input: amount. How many features should the function display.
		Displays the most informative features in the classifier used
		to classify each tweet.
		"""
		
		self.classifier.show_most_informative_features( amount )
	
	
	def __init_naive_bayes(self):
		"""
		__init_naive_bayes(self):
		Gets the data from the positive, negative and neutral text files.
		Creates and trains the Naive Bayes classifier, using the data, so 
		that it can learn what constitutes a positive, negative or neutral tweet.
		"""
		
		try:
			pos_file = pjoin( sys.path[0], "sentiment_word_files", "tweets_positive.txt")
			f = codecs.open( pos_file, mode="rU", encoding='utf-8')
			positive = [ line.lower().replace("\n" , " ") for line in f ]
			positive = "".join(word[:] for word in positive).split()
			f.close
		
			neu_file = pjoin( sys.path[0], "sentiment_word_files", "tweets_neutral.txt")
			f = codecs.open( neu_file, mode="rU", encoding='utf-8')
			neutral = [ line.lower().replace("\n" , " ") for line in f ]
			neutral = "".join(word[:] for word in neutral).split()
			f.close
		
			neg_file = pjoin( sys.path[0], "sentiment_word_files", "tweets_negative.txt")
			f = codecs.open( neg_file, mode="rU", encoding='utf-8')
			negative = [ line.lower().replace("\n" , " ") for line in f ]
			negative = "".join(word[:] for word in negative).split()
			f.close
		
			posfeats = [( dict( { word.lower() : True } ), 'pos' ) for word in positive if self.__check_word( word ) ]
			neufeats = [( dict( { word.lower() : True } ), 'neu' ) for word in neutral if self.__check_word( word ) ]
			negfeats = [( dict( { word.lower() : True } ), 'neg' ) for word in negative if self.__check_word( word ) ]
		
			self.classifier = NaiveBayesClassifier.train( posfeats + neufeats + negfeats )
		
		except:
			raise Exception ("Unknown error in SentimentAnalyzer::__init_naive_bayes")
	
	def __check_word( self, word ):
		"""
		__check_word( self, word ):
		Input: word. The word to check.
		Looks at a word and determines whether that should be used in the classifier.
		Return: True if the word should be used, False if not.
		"""
		if word in self.stopSet \
			or len(word) < self.min_word_length \
			or word[0] == "@" \
			or word[0] == "#" \
			or word[:4] == "http":
				return False
		else:
			return True
	
	
	
	def __analyze_tweet(self, tweet):
		"""
		__analyze_tweet(self, tweet):
		Input: tweet. The tweet that should be analyzed.
		Analyses a tweet using the created Naive Bayes classifier.
		Return: The results fromt the classifier. Possible results: 'pos', 'neg' or 'neu'
		"""
		try:
			tweet_features = dict([ (word, True) 
							for word in tweet.lower().split() 
							if self.__check_word( word ) ] )
			return self.classifier.classify( tweet_features )
		
		except:
			raise Exception ("Unknown error in SentimentAnalyzer::__analyze_tweet")
			return 'err'
	
	
	def __analyse_using_naive_bayes(self, data):
		"""
		__analyse_using_naive_bayes(self, data):
		Input: data. A list of tweets to analyze.
		Takes a list of tweets and uses sentiment analysis to determine 
		whether each tweet is positive, negative or neutral.
		Return: A list of the tweets analyzed.
		"""
		analyzed_data = {}
		try:
			for search_term, tweet_data in data.iteritems():
				self.results[search_term + "_positive"] = 0
				self.results[search_term + "_negative"] = 0
				self.results[search_term + "_neutral"] = 0
			
				search_term_data = []
				for data in tweet_data:
					temp_data = data
					result = self.__analyze_tweet( data[0] )
					temp_data.append( result )
					search_term_data.append( temp_data )
				
					if (result == 'pos'): self.results[search_term + "_positive"] += 1
					elif (result == 'neg'): self.results[search_term + "_negative"] += 1
					elif (result == 'neu'): self.results[search_term + "_neutral"] += 1
			
				analyzed_data[search_term] = search_term_data
				self.results["positive"] += self.results[search_term + "_positive"]
				self.results["negative"] += self.results[search_term + "_negative"]
				self.results["neutral"] += self.results[search_term + "_neutral"]
			
			return analyzed_data
		
		except:
			raise Exception ("Unknown error in SentimentAnalyzer::__analyse_using_naive_bayes")
			return analyzed_data
