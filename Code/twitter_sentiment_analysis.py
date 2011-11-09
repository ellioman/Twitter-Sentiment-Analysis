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


#Key variables
pages = 5
results_per_page = 100
english_tweets_count = 0
search_terms = ["Wayne Rooney MUFC", "Wayne Rooney"]
html_filename = "DataMiningResults.html"
template_filename = "template.html"


def main():
	"""Main function for the program"""
	tweets = twitter_aggregator()
	
	print "=======================\nData mining starting\n=======================\n"
	
	print "Searching..."
	tweets.twitter_search( search_terms=search_terms, pages=pages, results_per_page=results_per_page )
	print "Search complete"
	
	#print "Saving data..."
	#raw_file, filtered_file = tweets.save_data( twitter_data, filtered_data )
	#print "Saving data complete"
	
	# Get all the tweets/data
	data = tweets.get_data( data_to_get=['text', 'profile_image_url', 'from_user'] )
	
	print "Creating HTML page..."
	html_page = HTMLCreator( html_filename, template_filename, data )
	html_page.create_html()
	print "Creating HTML page complete\n"
	
	print "=======================\nData mining successful\n=======================\n"


if __name__ == '__main__':
	main()
