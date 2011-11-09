# encoding: utf-8
"""
html_creator.py

Created by Elvar Örn Unnþórsson on 2011-09-13.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import nltk
import random
from cgi import escape
from mako.template import Template
from os.path import join as pjoin

class HTMLCreator(object):
	"""
	Class to create HTML out of twitter data.
	Must provide the class with the following:
	* Name of the html page to create
	* Name of the template for the html to follow. The template must have: 
	    * <ul id="cloud"> to place the word cloud
	    * <div class="tweets"> to place the tweets
	* Twitter data consisting of list of [tweet text, profile pic, user name] lists
	"""
	
	def __init__(self, page_name, template_name, twitter_data, stats):
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
		self.word_cloud_max_words = 100
		self.stats = stats
	
	
	
	def create_html(self):
		"""docstring for create_html"""
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
		f = open( self.page_name, "wb")
		f.write(Template("${data}").render(data=html))
		f.close()
	
	
	def __create_stats_info(self):
		"""docstring for __create_stats_info"""
		self.stats_html = "\n"
		self.stats_html += '\t\t\t\t\t\tSearch parameters: <br/>\n'
		self.stats_html += '\t\t\t\t\t\t<ul class="search-parameters">\n'
		
		for term in self.stats["search-parameters"]:
			self.stats_html += "\t\t\t\t\t\t\t<li>" + term + "</li>\n"
		
		self.stats_html += '\t\t\t\t\t\t</ul>\n'
		self.stats_html += '\t\t\t\t\t\tTweets count: ' + str(self.stats["tweets-count"]) + '<br/>\n'
		self.stats_html += '\t\t\t\t\t\tPositive tweets: ' + str(self.stats["positive-count"]) + '<br/>\n'
		self.stats_html += '\t\t\t\t\t\tNegative tweets: ' + str(self.stats["negative-count"]) + '<br/>'
	
	
	def __create_tweet_list(self):
		"""docstring for __Create_tweet_list"""
		count = 1
		
		for data in self.twitter_data:
			if ( count % 3 == 0 ):
				self.tweets += '\n\t\t\t\t\t<div class="left-tweets">\n'
				self.tweets += '\t\t\t\t\t\t<div class="tweet-positive">\n'
				
			else:
				self.tweets += '\n\t\t\t\t\t<div class="right-tweets">\n'
				self.tweets += '\t\t\t\t\t\t<div class="tweet-negative">\n'
			
			self.tweets += '\t\t\t\t\t\t\t<div class="img">\n\t\t\t\t\t\t\t\t<img src="'\
			 				+ data[1] + '" width="50px"/>\n\t\t\t\t\t\t\t</div>\n' # Image
			self.tweets += '\t\t\t\t\t\t\t<div class="author"><a href="http://twitter.com/#!/'\
			 				+ data[2] + '">' + data[2] + '</a></div>\n' # Author's name
			self.tweets += '\t\t\t\t\t\t\t<div class="text">\n\t\t\t\t\t\t\t\t'\
			 				+ data[0] + '\n\t\t\t\t\t\t\t</div>\n' # Tweet
			self.tweets += '\t\t\t\t\t\t</div>\n'
			self.tweets += '\t\t\t\t\t</div>'
			
			if ( count % 3 == 0 ):
				self.tweets += '\n\t\t\t\t\t<br class="clear">'
			count += 1
		self.tweets += '\n\t\t\t\t\t<br class="clear">'
	
	
	def __create_word_cloud(self):
		"""docstring for test"""
		MIN_FREQUENCY = self.word_cloud_min_frequency
		MIN_FONT_SIZE = self.word_cloud_min_font_size
		MAX_FONT_SIZE = self.word_cloud_max_font_size
		MAX_WORDS = self.word_cloud_max_words
		
		# Get all words from the tweet search and put them in a list
		tweets = []
		for tweet_data in self.twitter_data:
			tweet_words = tweet_data[0].split()
			
			# Append the words in lowercase to remove duplicates
			for word in tweet_words: tweets.append( word.lower() ) 
		
		
		# Compute frequency distribution for the terms
		fdist = nltk.FreqDist([term for t in tweets for term in t.split()])
		
		# Customize a list of stop words as needed
		stop_words = nltk.corpus.stopwords.words('english')
		stop_words += ['&', '&amp;', '.', '..','...','...', '?', '!', ':', '"', '&quot;', '(', ')', '()', '-', '--']
		stop_words += ["RT"] # Common Twitter words
		
		
		# Create output for the WP-Cumulus tag cloud and sort terms by freq
		raw_output = sorted([ [term, '', freq] for (term, freq) in fdist.items()
							  if freq > MIN_FREQUENCY and term not in stop_words and len(term) >= 3], 
							  key=lambda x: x[2])
		
		# Scale the font size by the min and max font sizes
		# Implementation adapted from 
		# http://help.com/post/383276-anyone-knows-the-formula-for-font-s
		def weightTermByFreq(f):
			return (f - min_freq) * (MAX_FONT_SIZE - MIN_FONT_SIZE) / (max_freq - min_freq) + MIN_FONT_SIZE
		
		min_freq = raw_output[0][2]
		max_freq = raw_output[-1][2]
		weighted_output = [[i[0], i[1], weightTermByFreq(i[2])] for i in raw_output]
		
		# Create the html list <li> for the results page
		myList = []
		for (tag, n, font_size) in weighted_output:
			myList.append( '\t\t\t\t\t\t\t<li class="tag%d">%s</li>' % (font_size, tag) )
		
		# Minimize the html list to the number specified,
		# randomize it and add it to the word cloud string
		myList = myList[-MAX_WORDS:]
		random.shuffle(myList)
		self.word_cloud = '\n'.join(tag[:] for tag in myList)
	
	
	
	def __sort_a_list(self, myList):
		"""Takes a list of words, counts each instance of it and returns a sorted list"""
		words = {}
		for x in (' '.join(myList)).split():
			words[x] = 1 + words.get(x, 0)
		return sorted(words.items(), key=lambda user: user[1], reverse=True)



if __name__ == '__main__':
	from twitter_aggregator import *
	tweets = twitter_aggregator()
	tweets.twitter_search( search_terms=["Wayne Rooney MUFC", "Wayne Rooney"], pages=1, results_per_page=60 )
	data = tweets.get_data( data_to_get=['text', 'profile_image_url', 'from_user', 'source'] )
	html_page = HTMLCreator( "DataMiningResults.html", "template.html", data )
	html_page.create_html()

