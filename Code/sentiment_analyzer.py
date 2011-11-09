#!/usr/bin/env python
# encoding: utf-8
"""
sentiment_analyzer.py

Created by Elvar Örn Unnþórsson on 2011-11-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os


class sentiment_analyzer:
	def __init__(self):
		self.positive_tweets = 666
		self.negative_tweets = 999
		self.data = []
	
	def analyze(self, data):
		"""docstring for analyze"""
		
		# For now it does nothing!
		self.data = data
	
	def get_analyzed_data(self):
		"""docstring for get_analyzed_data"""
		return self.data


if __name__ == '__main__':
	unittest.main()