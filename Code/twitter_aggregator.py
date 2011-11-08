#!/usr/bin/env python
# encoding: utf-8
"""
twitter_aggregator.py

Created by Elvar Örn Unnþórsson on 2011-09-27.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import datetime
import twitter
import thread
import time
from os.path import join as pjoin


class twitter_aggregator:
	def __init__( self ):
		self.data = []
		self.english_tweets_count = 0
		self.raw_data_directory_name = "raw_mining_data"
		self.filtered_data_directory_name = "filtered_mining_data"
	
	
	
	def twitter_search( self, search_terms = [], pages = 1, results_per_page = 100 ):
		"""docstring for twitter_search"""
		if search_terms == []: return ''
		
		twitter_search = twitter.Twitter(domain="search.twitter.com")
		search_results = []
		done_searching = False
		
		def print_time( delay ):
			while done_searching == False:
				time.sleep(delay)
				print "."
		
		thread.start_new_thread( print_time, ( 0.5, ) )
		
		for term in search_terms:
			for page in range(1,pages+1):
				search_results.append(twitter_search.search(q=term, rpp=results_per_page, page=page))
		
		done_searching = True
		
		self.data = search_results
	
	
	
	def get_data(self, data_to_get = []):
		"""docstring for get_data"""
		tweet_list = []
		for page in range( len(self.data) ):
			for tweet in range( len(self.data[page]['results']) ):
				tweet_data = []
				for data in data_to_get:
					tweet_data.append( self.data[page]['results'][tweet][data].encode('ascii', 'ignore') )
				tweet_list.append(tweet_data)
		return tweet_list
	
	
	
	def save_data( self, twitter_data, filtered_data ):
		"""docstring for save_data"""
		date = str( datetime.datetime.today() )[:-7].split()
		filename = "Search-date_"+date[0][-2:]+date[0][-5:-3]+date[0][:-6]+"_time_"+date[1][:-6]+date[1][3:5]+date[1][6:]+".txt"
		
		raw_file = pjoin(sys.path[0], self.raw_data_directory_name, filename)
		self.save_to_file(str(twitter_data), raw_file )
		
		filtered_file = pjoin(sys.path[0], self.filtered_data_directory_name, filename)
		self.save_to_file(filtered_data, filtered_file )
		
		return raw_file, filtered_file
	
	
	
	def save_to_file( self, text_to_save = "", path_and_filename = "fileToSave.txt" ):
		"""This function saves a text string to a file."""
		f = open(path_and_filename, "wb")
		f.write(text_to_save)
		f.close



if __name__ == '__main__':
	tweets = twitter_aggregator()
	tweets.twitter_search( search_terms=['MUFC'], pages=2, results_per_page=2 )
	print tweets.get_data( ['from_user', 'iso_language_code', 'from_user_id'] )