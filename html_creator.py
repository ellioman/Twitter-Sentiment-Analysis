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
	
	def __init__(self, page_name, template_name, twitter_data):
		super(HTMLCreator, self).__init__()
		self.page_name = page_name
		self.template_name = template_name
		self.twitter_data = twitter_data
		self.tweets = ""
		self.word_cloud = ""
	
	
	
	def create_html(self):
		"""docstring for create_html"""
		f = open( pjoin(sys.path[0], "html/template", self.template_name), "r")
		html = f.read()
		f.close
		
		# Append the word cloud to the html
		self.__create_word_cloud()
		index = html.find('<ul id="cloud">') + len('<ul id="cloud">')
		html_before_cloud, html_after_cloud = html[:index], html[index:]
		html = html_before_cloud + self.word_cloud + html_after_cloud
		
		# Append the tweets to the html
		self.__create_tweet_list()
		index = html.find('<div class="tweets">') + len('<div class="tweets">')
		html_before_tweets, html_after_tweets = html[:index], html[index:]
		html = html_before_tweets + self.tweets + html_after_tweets
		
		# Create and save the html file
		f = open( self.page_name, "wb")
		f.write(Template("${data}").render(data=html))
		f.close
		
	
	
	
	def __create_tweet_list(self):
		"""docstring for __Create_tweet_list"""
		for data in self.twitter_data:
			self.tweets += '<div class="tweet">'
			self.tweets += '<div class="img"><img src="' + data[1] + '"/></div>' # Image
			self.tweets += '<div class="author"><a href="http://twitter.com/#!/' + data[2] + '"> ' + data[2] + '</a></div>' # Author's name
			self.tweets += '<div class="text">' + data[0] + '</div>' # Tweet
			self.tweets += '</div>'
	
	
	
	def __create_word_cloud(self):
		stopwords = nltk.corpus.stopwords.words('english')
		punct = ['.', '..', '...', ',', '!', '?', ';', ':', '-', '=', '(', ')', '|', ':-']
		
		tweets_without_user = ''
		for tweet in self.twitter_data:
			tweets_without_user += tweet[0] + ' '
		
		tweets_without_user = tweets_without_user.split()
		
		#Remove punctuation
		for index, word in enumerate(tweets_without_user):
			for pun in punct:
				if pun in word:
					tweets_without_user[index] = word.replace(pun, '')
		
		# Remove all empty tags
		for index, word in enumerate(tweets_without_user):
			if word == '':
				tweets_without_user.pop(index)
		
		# Put the tags into a dictionary to remove duplicates
		tags = self.__sort_a_list(tweets_without_user)
		tags = [w[0] for w in tags if w[0].lower() not in stopwords]
		
		# Remove words that are 3 or less letters
		remove_list = []
		for index, word in enumerate(tags):
			if len(word) < 4:
				remove_list.append(word)
		
		for word in remove_list:
			tags.remove( word )
		 
		
		# Create the html list
		myList = []
		for i in range(10):
			for x in range(10):
				myList.append( '<li class="tag%d">%s</li>' % (10-i, tags[i*10+x]) )
		
		# Randomize the list
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
	tweets.twitter_search( search_terms=["MUFC"], pages=1, results_per_page=10 )
	html_page = HTMLCreator( "DataMiningResults.html", "template.html", tweets.get_data( data_to_get=['text', 'profile_image_url', 'from_user', 'source'] ) )
	#html_page.create_html()

