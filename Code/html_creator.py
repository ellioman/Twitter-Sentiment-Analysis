#!/usr/bin/env python
# encoding: utf-8
"""
html_creator.py

Created by Elvar Orn Unnthorsson on 07-12-2011
Copyright (c) 2011 ellioman inc. All rights reserved.
"""

import sys
import os
import nltk
import random
from cgi import escape
from os.path import join as pjoin
from mako.template import Template


class HTMLCreator(object):
	
	"""
	HTMLCreator creates a HTML webpage that displays statistics, word cloud and a list of all
	tweets harvested. Must provide the class with the following:
	* Name of the html page to create
	* Name of the template for the html to follow. The template must have: 
	    * <ul id="cloud"> to place the word cloud
	    * <div class="tweets"> to place the tweets
	* Twitter data consisting of list of [tweet text, profile pic, user name] lists
	"""
	
	def __init__( self, page_name, template_name, twitter_data, stats ):
		"""
		Constructs a new HTMLCreator instance.
		"""
		
		super(HTMLCreator, self).__init__()
		self.page_name = page_name
		self.template_name = template_name
		self.twitter_data = twitter_data
		self.tweets = ""
		self.word_cloud = ""
		self.stats_html = ""
		self.word_cloud_min_frequency = 5
		self.word_cloud_min_font_size = 1
		self.word_cloud_max_font_size = 25
		self.word_cloud_max_words = 30
		self.word_cloud_min_word_length = 3
		self.stats = stats
	
	
	def create_html( self ):
		"""
		create_html(self):
		Creates the webpage used to show the results from the twitter search and analysis.
		"""
		try: 
			f = open( pjoin(sys.path[0], "html/template", self.template_name), "r")
			html = f.read()
			f.close
			
			# Put the stats in the html
			self.__create_stats_info()
			index = html.find('<div id="stats">') + len('<div id="stats">')
			html_before_stats, html_after_stats = html[:index], html[index:]
			html = html_before_stats + self.stats_html + html_after_stats
			
			# Append the word cloud to the html
			self.__create_word_cloud()
			index = html.find('<ul id="cloud">') + len('<ul id="cloud">')
			html_before_cloud, html_after_cloud = html[:index], html[index:]
			html = html_before_cloud + '\n' + self.word_cloud + html_after_cloud
			
			# Append the tweets to the html
			self.__create_tweet_list()
			index = html.find('<div class="tweet-container">') + len('<div class="tweet-container">')
			html_before_tweets, html_after_tweets = html[:index], html[index:]
			html = html_before_tweets + self.tweets + html_after_tweets
			
			# Create and save the html file
			f = open( pjoin(sys.path[0], "html", self.page_name), "wb")
			f.write(Template("${data}").render(data=html))
			f.close()
		
		except:
			raise Exception ("Unknown error in HTMLCreator::create_html")
	
	
	def __create_stats_info( self ):
		"""
		__create_stats_info(self):
		Creates the statistics part of the webpage.
		"""
		try:
			self.stats_html = '\n' + '\t'*6
			self.stats_html += '<strong>Search parameters</strong>\n'
			self.stats_html += '\t'*6 + '<br/>\n'
			self.stats_html += '\t'*6 + '<ul class="search-parameters">\n'
			
			for term in self.stats["search_parameters"]:
				self.stats_html += '\t'*7 + '<li>' + term + "</li>\n"
			
			self.stats_html += '\t'*6 + '</ul>\n'
			self.stats_html += '\t'*6 + 'Tweets count: '
			self.stats_html += str(self.stats["tweets_count"]) + '\n'
			self.stats_html += '\t'*6 + '<br/>\n'
			self.stats_html += '\t'*6 + 'Positive tweets: '
			self.stats_html += str(self.stats["positive_count"]) + '\n'
			self.stats_html += '\t'*6 + '<br/>\n'
			self.stats_html += '\t'*6 + 'Neutral tweets: '
			self.stats_html += str(self.stats["neutral_count"]) + '\n'
			self.stats_html += '\t'*6 + '<br/>'
			self.stats_html += '\t'*6 + 'Negative tweets: '
			self.stats_html += str(self.stats["negative_count"]) + '\n'
			self.stats_html += '\t'*6 + '<br/>'
		
		except:
			raise Exception ("Unknown error in HTMLCreator::__create_stats_info")
	
	
	def __create_tweet_list( self ):
		"""
		__create_tweet_list(self):
		Creates the tweet listing part of the webpage.
		"""
		
		count = 1
		try:
			# For each result from the search...
			for search_term, results in self.twitter_data.iteritems():
				
				# For each tweet in the results...
				for tweet_data in results:
					
					# Make sure that the comments are in rows of three elements
					if ( count % 3 == 0 ):
						self.tweets += '\n' + '\t'*5 + '<div class="left-tweets">\n'
					else:
						self.tweets += '\n' + '\t'*5 + '<div class="right-tweets">\n'
					
					# See if it's a positive, negative or neutral tweet and 
					# put appropriate html class for the tweet
					if ( tweet_data[3] == "pos" ):
						self.tweets += '\t'*6 + '<div class="tweet-positive">\n'
					elif ( tweet_data[3] == "neg" ):
						self.tweets += '\t'*6 + '<div class="tweet-negative">\n'
					elif ( tweet_data[3] == "neu" ):
						self.tweets += '\t'*6 + '<div class="tweet-neutral">\n'
					
					# Image
					self.tweets += '\t'*7 + '<div class="img">\n' + '\t'*8
					self.tweets +='<img src="' + tweet_data[1] + '" width="50px"/>\n'
					self.tweets += '\t'*7 + '</div>\n'
					
					# Author's name
					self.tweets += '\t'*7 + '<div class="author">\n' + '\t'*8 
					self.tweets += '<a href="http://twitter.com/#!/' + tweet_data[2]
					self.tweets += '">' + tweet_data[2] + '</a>\n' + '\t'*7 + '</div>\n' 
					# Tweet text
					self.tweets += '\t'*7 + '<div class="text">\n' + '\t'*7
					self.tweets += tweet_data[0] + '\n' + '\t'*7 + '</div>\n' 
					self.tweets += '\t'*6 + '</div>\n'
					self.tweets += '\t'*5 + '</div>'
					
					if ( count % 3 == 0 ):
						self.tweets += '\n' + '\t'*5 + '<br class="clear">'
					count += 1
			
			self.tweets += '\n' + '\t'*5 + '<br class="clear">'
		
		except:
			raise Exception ("Unknown error in HTMLCreator::__create_tweet_list")
	
	
	def __create_word_cloud( self ):
		"""
		__create_word_cloud( self ):
		Creates the word cloud part of the webpage. Takes the 30 most
		frequent words used and assigns the relevant class to it.
		"""
		
		MIN_FREQUENCY = self.word_cloud_min_frequency
		MIN_FONT_SIZE = self.word_cloud_min_font_size
		MAX_FONT_SIZE = self.word_cloud_max_font_size
		MAX_WORDS = self.word_cloud_max_words
		MIN_WORD_LENGTH = self.word_cloud_min_word_length
		
		try:
			# Get all words from the tweet search and put them in a list
			tweets = []
			for search_term, results in self.twitter_data.iteritems():
			
				for tweet_data in results:
					tweet_words = tweet_data[0].split()
				
					# Append the words in lowercase to remove duplicates
					for word in tweet_words:
						tweets.append( word.lower() ) 
		
			# Compute frequency distribution for the terms
			fdist = nltk.FreqDist([term for t in tweets for term in t.split()])
		
			# Customize a list of stop words as needed
			stop_words = nltk.corpus.stopwords.words('english')
			stop_words += ['&', '&amp;', '.', '..','...','...', '?', '!', ':', '"', '&quot;', '(', ')', '()', '-', '--']
			stop_words += ["RT"] # Common Twitter words
		
		
			# Create output for the WP-Cumulus tag cloud and sort terms by freq
			raw_output = sorted([ [term, '', freq] for (term, freq) in fdist.items()
								  if freq > MIN_FREQUENCY 
									and term not in stop_words 
									and len(term) >= MIN_WORD_LENGTH], 
								  key=lambda x: x[2])
		
			# Scale the font size by the min and max font sizes
			# Implementation adapted from 
			# http://help.com/post/383276-anyone-knows-the-formula-for-font-s
			def weightTermByFreq(f):
				return (f - min_freq) * \
				 		(MAX_FONT_SIZE - MIN_FONT_SIZE) / \
				 		(max_freq - min_freq) + MIN_FONT_SIZE
		
			min_freq = raw_output[0][2]
			max_freq = raw_output[-1][2]
			weighted_output = [[i[0], i[1], weightTermByFreq(i[2])] for i in raw_output]
		
			# Create the html list <li> for the results page
			myList = []
			for (tag, n, font_size) in weighted_output:
				myList.append( '\t'*7 + '<li class="tag%d">%s</li>' % (font_size, tag) )
		
			# Minimize the html list to the number specified,
			# randomize it and add it to the word cloud string
			myList = myList[-MAX_WORDS:]
			random.shuffle(myList)
			self.word_cloud = '\n'.join(tag[:] for tag in myList)
		
		except:
			raise Exception ("Unknown error in HTMLCreator::__create_word_cloud")
