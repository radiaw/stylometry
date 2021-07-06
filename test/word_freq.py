#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Common imports
import numpy as np
import pandas as pd
import numpy.random as rnd
import matplotlib.pyplot as plt
import math
import re

# Load nltk
import nltk
nltk.download('punkt')
nltk.download('stopwords')


fname = input("Enter file name (Default Sanderson's Mistborn Trilogy):")

if fname == "":
    fname = "Sanderson_00"

strings = ""
counter = 1
with  open(f'../data/{fname}.txt') as f:
    strings = f.read()
    tokens  = nltk.word_tokenize(strings)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered = [token.lower() for token in tokens if not token.lower() in stop_words]
    tokenlist = [token for token in filtered  if token.isalpha()]

    # Get a frequency distribution
    wordfreq = list(nltk.FreqDist(tokenlist).most_common(n = 300))
    print(wordfreq)
    stop_words = set(nltk.corpus.stopwords.words('english'))

    # Print the Feature Frequency Distribution in all books
    print(f"\nThe Feature Frequency Distribution in {fname}.txt:\n")
    print("  Index       Feature       Frequency")
    print("---------+--------------+---------------")
    for index, (word, count) in enumerate(wordfreq):
        print("%5d   %12s%s" % (index, word.upper(), '{:15,}'.format(count)))
    print("\n")
