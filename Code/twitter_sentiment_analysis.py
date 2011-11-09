# encoding: utf-8
"""
twitter_sentiment_analysis.py

Created by Elvar Örn Unnþórsson on 2011-09-12.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import twitter
import nltk
from twitter_aggregator import *
from html_creator import *
from sentiment_analyzer import *

#Key variables
pages = 1
results_per_page = 60
search_terms = ["Wayne Rooney", "Carrick", "Alex Ferguson"]
html_filename = "DataMiningResults.html"
template_filename = "template.html"


def main():
	"""Main function for the program"""
	
	print "=======================\nData mining starting\n=======================\n"
	
	print "Searching..."
	tweets = twitter_aggregator()
	tweets.twitter_search( search_terms=search_terms, pages=pages, results_per_page=results_per_page )
	print "Search complete"
	
	#print "Saving data..."
	#raw_file, filtered_file = tweets.save_data( twitter_data, filtered_data )
	#print "Saving data complete"
	
	# Get all the tweets/data
	data = tweets.get_data( data_to_get=['text', 'profile_image_url', 'from_user'] )
	
	# Analyze the data
	print "Analyzing the data..."
	analyzer = sentiment_analyzer()
	analyzer.analyze(data)
	data = analyzer.get_analyzed_data()
	print "Analyzing complete"
	
	# A Statistic dictionary, used to print out 
	# the information on the results webpage.
	stats = {}
	stats["search-parameters"] = search_terms
	stats["tweets-count"] = len(data)
	stats["positive-count"] = analyzer.positive_tweets
	stats["negative-count"] = analyzer.negative_tweets
	
	print "Creating HTML page..."	
	html_page = HTMLCreator( html_filename, template_filename, data,stats )
	html_page.create_html()
	print "Creating HTML page complete\n"
	
	print "=======================\nData mining successful\n=======================\n"


if __name__ == '__main__':
	main()
