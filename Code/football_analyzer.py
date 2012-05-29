#!/usr/bin/env python
# encoding: utf-8
"""
02820 Python Programming

twitter_sentiment_analysis.py

Created by Elvar Orn Unnthorsson on 07-12-2011
Copyright (c) 2011 ellioman inc. All rights reserved.
"""

import sys
import os
import twitter
import nltk
import thread
from twitter_aggregator import *
from html_creator import *
from sentiment_analyzer import *

class FootballAnalyzer:
	
	"""
	FootballAnalyzer is searches twitter for tweets, performs a 
	sentiment analysis of each tweet harvested and creates a webpage,
	in the folder \"html\" that shows the results.
	"""
	
	def __init__( self, search_terms = [], pages = 3, results_per_page = 50 ):
		"""
		Input: search_terms. A list of search terms to for searching Twitter.
		Input: pages. A Number that determines how many pages of tweets to search for.
		Input: results_per_page. A Number which determines how many tweet results should be on each page.
		Constructs a new FootballAnalyzer instance.
		"""
		
		self.html_filename = "DataMiningResults.html"
		self.template_filename = "template.html"
		self.task_finished = False
		self.search_terms = search_terms
		self.pages = pages
		self.results_per_page = results_per_page
	
	
	def run( self ):
		"""
		run( self ):
		Runs the football analyzer. Searches, analyzes and creates the webpage.
		"""
		
		print "=======================\nData mining starting\n=======================\n"
		tweets = self.__search()
		analyzed_tweets = self.__analyze( tweets )
		self.__create_webpage( analyzed_tweets )
		
		print "=======================\nData mining successful\n=======================\n"
	
	
	def __search( self ):
		"""
		__search( self ):
		Creates a search aggregator instance and performs a twitter search using the
		the search parameters given in the constructor. Returns a list of the tweets harvested.
		Return: A list of all tweets harvested.
		"""
		
		try:
			print "Searching..."
			self.__start_task();
			self.aggregator = TwitterAggregator()
			self.aggregator.twitter_search( search_terms=self.search_terms, pages=self.pages, results_per_page=self.results_per_page )
			
			tweets = {} 
			for term in self.search_terms:
				tweets[term] = self.aggregator.get_tweets( search_terms = [ term ], return_all_tweets = True  )
			self.__end_task();
			print "Search complete"
			
			return tweets
		
		except:
			raise Exception ("Unknown error in FootballAnalyzer::__search")
	
	
	def __analyze( self, tweets ):
		"""
		__analyze( self, tweets ):
		Input: tweets. A list of tweets strings
		Creates a sentiment analyzer instance and uses it to analyze each tweet harvested 
		by the twitter aggregator. it returns a list of the analyzed tweets.
		Return: A list of the tweets analyzed. 
		"""
		
		try:
			print "Analyzing the data..."
			self.__start_task();
			self.analyzer = SentimentAnalyzer()
			analyzed_tweets = self.analyzer.analyze( tweets )
			self.__end_task();
			print "Analyzing complete"
			
			self.analyzer.show_most_informative_features( 20 )
			
			return analyzed_tweets
		
		except:
			raise Exception ("Unknown error in FootballAnalyzer::__analyze")
	
	
	def __create_webpage( self, analyzed_tweets ):
		"""
		__create_webpage( self, analyzed_tweets ):
		Input: analyzed_tweets. A list of tweets strings
		Creates a webpage with statistics gathered from the tweet aggregator and analyzer,
		a word cloud with the 30 most used words in the tweets and list of each tweet harvested
		which are colored green, red and white depending on the results from the analyzer.
		"""
		
		try:
			print "Creating HTML page..."
			self.__start_task();
			
			# A Statistic dictionary, used to print out the information on the results webpage.
			stats = {}
			stats["search_parameters"] = self.search_terms
			stats["tweets_count"] = self.aggregator.tweets_count
			stats["positive_count"] = self.analyzer.get_analysis_result( "positive" )
			stats["negative_count"] = self.analyzer.get_analysis_result( "negative" )
			stats["neutral_count"] = self.analyzer.get_analysis_result( "neutral" )
			
			html_page = HTMLCreator( self.html_filename, self.template_filename, analyzed_tweets, stats )
			html_page.create_html()
			self.__end_task();
			
			print "Creating HTML page complete\n"
		
		except:
			raise Exception ("Unknown error in FootballAnalyzer::__create_webpage")
	
	
	def __start_task( self ):
		"""
		__start_task( self ):
		Creates a thread which displays dots while a function in the FootballAnalyzer is running.
		"""
		
		self.task_finished = False
		thread.start_new_thread( self.__print_time, ( 1.0, ) )
	
	
	def __end_task( self ):
		"""
		__end_task( self ):
		Stops the thread created in the __start_task() function.
		"""
		
		self.task_finished = True
		time.sleep( 1.0 )
	
	
	def __print_time( self, delay ):
		"""
		__print_time( self, delay ):
		Input: delay. A number which determines how much time should be between the dot printing
		Prints dots while a function in the FootballAnalyzer is running.
		"""
		
		while not self.task_finished:
			print "."
			time.sleep( delay )


if __name__ == '__main__':
	search = [ "Rooney bad" ]
	page_per_search = 3
	results_on_page = 10
	f = FootballAnalyzer( search_terms = search, pages = page_per_search, results_per_page = results_on_page )
	f.run()