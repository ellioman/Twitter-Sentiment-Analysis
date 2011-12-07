#!/usr/bin/env python
# encoding: utf-8
"""
twitter_aggregator.py

Created by Elvar Orn Unnthorsson on 07-12-2011
Copyright (c) 2011 ellioman inc. All rights reserved.
"""

import string
import sys
import os
import re
import datetime
import twitter
import time
import redis
from os.path import join as pjoin
import ast


class TwitterAggregator:
	
	"""
	TwitterAggregator performs a Twitter GET Search and harvests tweets using the search parameters 
	given to it. It saves the twitter data, from the search, to a redis database and allows the user
	to get the data by calling the function "get_tweets()".
	"""
	
	def __init__( self ):
		"""
		Constructs a new TwitterAggregator instance.
		"""
		
		self.redis = redis.Redis()
		self.info_to_get = ['text', 'profile_image_url', 'from_user']
		self.search_results = {}
		self.raw_data_directory_name = "raw_mining_data"
		self.filtered_data_directory_name = "filtered_mining_data"
		english_file = pjoin( sys.path[0], "sentiment_word_files", "Nielsen2010Responsible_english.csv")
		self.analyzeEnglish = dict(map(lambda (w,e): (w, int(e)), \
									[ line.strip().lower().split('\t') for line in open(english_file) ]))
		self.tweets_count = 0
	
	
	def twitter_search( self, search_terms = [], pages = 1, results_per_page = 100 ):
		"""
		twitter_search( self, search_terms = [], pages = 1, results_per_page = 100 ):
		Input: search_terms. A list of search terms to for searching Twitter.
		Input: pages. A Number that determines how many pages of tweets to search for.
		Input: results_per_page. A Number which determines how many tweet results should be on each page.
		Searches twitter for the things listed in the search_terms list and saves 
		the data collected, in a Redis database.
		"""
		
		if search_terms == []: return ''
		
		self.pages = pages
		self.results_per_page = results_per_page
		twitter_search = twitter.Twitter( domain="search.twitter.com" )
		search_results = []
		
		try:
			# For each search term...
			for term in search_terms:
				results = []
				for page in range( 1, pages+1 ):
					results.append(twitter_search.search( q=term, rpp=results_per_page, page=page, result_type="recent" ) )
			
				# Get the tweets from the search
				new_tweets_ids = self.__get_tweet_ids( search_results=results )
				
				# Save tweets and other information to the database
				term_redis_name = term.replace( " ", "_" )
				term_tweetsIds_name = term_redis_name + "$TweetIds"
				term_searchcount_name = term_redis_name + "$SearchCount"
			
				if self.redis.exists( term_redis_name ):
					current_tweets_ids = ast.literal_eval( self.redis.get( term_tweetsIds_name ) )
					current_tweets_ids.append( new_tweets_ids )
					self.redis.set( term_tweetsIds_name, current_tweets_ids )
					self.redis.set( term_searchcount_name, int( self.redis.get( term_searchcount_name ) ) + 1 )
				else:
					self.redis.set( term_redis_name, True )
					self.redis.set( term_tweetsIds_name, [new_tweets_ids] )
					self.redis.set( term_searchcount_name, 1 )
		
		except:
			raise Exception ("Unknown error in TwitterAggregator::twitter_search")
	
	
	def get_tweets( self, search_terms = [], return_all_tweets = True ):
		""" 
		get_tweets( self, search_terms = [], return_all_tweets = True ):
		Input: search_terms. A list of search terms to fetch from the database.
		Input: return_all_tweets. Boolean that determines wether to get all tweets or from the last search.
		Fetches from the database each tweet text, username and url to the user's display pictures for each
		search term given in the "search_term" parameter.
		Return: A list which contains lists that has each tweet text, username and url to profile picture.
		"""
		
		returnList = []
		
		# If the search term list is empty, return an emptylist.
		if search_terms == []: return []
		
		try:
			# If not then get information about each tweet and put it in a list.
			for term in search_terms:
				term_redis_name = term.replace( " ", "_" )
				# Skip if the search term isn't in the database
				if not self.redis.exists( term_redis_name ): 
					print "Error: The search term", term, "does has not been searched for before..."
					continue
			
				term_tweetsIds_name = term_redis_name + "$TweetIds"
				tweet_searches = ast.literal_eval( self.redis.get(term_tweetsIds_name) )
			
				if return_all_tweets:
					ids = list( set( [ t_id for results in tweet_searches for t_id in results ] ) )
					tweet_info = [ self.redis.get( t_id ) for t_id in ids ]
				
					for t in tweet_info:
						returnList.append( ast.literal_eval( t ) )
						self.tweets_count += 1
			
				else:
					ids = list( set( [ t_id for t_id in tweet_searches[ len(tweet_searches)-1 ] ] ) )
					tweet_info = [ self.redis.get( t_id ) for t_id in ids ]
				
					for t in tweet_info:
						returnList.append( ast.literal_eval( t ) )
						self.tweets_count += 1
			
			return returnList
		
		except:
			raise Exception ("Unknown error in TwitterAggregator::__get_tweet_ids")
			return []
	
	
	def __get_tweet_ids( self, search_results = [] ):
		"""
		__get_tweet_ids( self, search_term = "", search_results = [] ):
		Input: search_results. A list with the JSON results from the Twitter API
		Fetches the tweet ids from the JSON results.
		Return: A list containing the ids found.
		"""
		
		# Return empty list if the list in the parameter is empty
		if search_results == []: return []
		
		count = 0
		tweet_ids = []
		non_english_tweets = 0
		
		try:
			# For each search result...
			for result in search_results:
			
				# For each tweet found...
				for tweet in result['results']:
					# Skip tweets that are not in english
					if not self.__is_english_tweet( tweet['text'] ) :
						continue
				
					tweet_info = []
					# Get each information data that was requested...
					for fetched_data in self.info_to_get:
						if ( type(tweet[fetched_data]) == int): tweet_info.append( tweet[fetched_data] )
						else: tweet_info.append( tweet[fetched_data].encode('ascii', 'ignore') )
				
					# Append the information to the gathered list
					tweet_ids.append( tweet['id_str'] )
				
					# Put the tweet info in the database with the string ID as key
					self.redis.set( tweet['id_str'], tweet_info )
			return tweet_ids
		
		except:
			raise Exception ("Unknown error in TwitterAggregator::__get_tweet_ids")
			return []
	
	
	def __is_english_tweet( self, tweet ):
		"""
		__is_english_tweet( self, tweet ):
		Input: tweet. A string containing a tweet to check.
		Determines whether a comment is an english one or not. This function 
		was given to the author by Helgi who is a fellow student at DTU.
		Return: True if english, False if not not english
		"""
		
		try:
			lang = sum(map(lambda w: self.analyzeEnglish.get(w, 0), \
				re.sub(r'[^\w]', ' ', string.lower(tweet)).split()))
				
			if lang >= 1.0: return True
			else: return False
		except:
			raise Exception ("Unknown error in TwitterAggregator::__isEnglishTweet")
			return False
