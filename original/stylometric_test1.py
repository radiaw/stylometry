#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Common imports
import load_dataset as ld
import numpy as np
import pandas as pd
import numpy.random as rnd
import matplotlib.pyplot as plt

# Load nltk
import nltk
nltk.download('punkt')

"""
Test 1: Mendenhall’s Characteristic Curves of Composition

Literary scholar T. C. Mendenhall once wrote that an author’s stylistic signature
could be found by counting how often he or she used words of different lengths.
For example, if we counted word lengths in several 1,000-word or 5,000 word segments
of any novel, and then plotted a graph of the word length distributions, the curves
would look pretty much the same no matter what parts of the novel we had picked.
Indeed, Mendenhall thought that if one counted enough words selected from various
parts of a writer’s entire life’s work (say, 100,000 or so), the author’s
“characteristic curve” of word length usage would become so precise that it would
be constant over his or her lifetime.

By today’s standards, counting word lengths seems like a very blunt way of measuring
literary style. Mendenhall’s method does not take the actual words in an author’s
vocabulary into account, which is obviously problematic. Therefore, we should not
treat the characteristic curves as a particularly trustworthy source of stylometric
evidence. However, Mendenhall published his theory over one hundred and thirty years
ago and made all calculations by hand. It is understandable that he would have chosen
to work with a statistic that, however coarse, was at least easy to compile. 
"""
def Mendenhall_Characteristicr_Curves_of_Composition():
    # Load dataset
    ld.dataset_load()

    # Compare the disputed papers to those written by everyone,
    # including the shared ones.
    authors = ("Hamilton", "Madison", "Disputed", "Jay", "Shared")

    # Transform the authors' corpora into lists of word tokens
    federalist_by_author_tokens = {}
    federalist_by_author_length_distributions = {}
    for author in authors:
        tokens = nltk.word_tokenize(ld.federalist_by_author[author])

        # Filter out punctuation
        federalist_by_author_tokens[author] = ([token for token in tokens
                                                if any(c.isalpha() for c in token)])

        # Get a distribution of token lengths
        token_lengths = [len(token) for token in federalist_by_author_tokens[author]]
        federalist_by_author_length_distributions[author] = nltk.FreqDist(token_lengths)
        print(federalist_by_author_length_distributions[author])
        print(federalist_by_author_length_distributions[author].keys())
        print(federalist_by_author_length_distributions[author].values())
        print("\n")
        federalist_by_author_length_distributions[author].plot(15,title=author)

if __name__ == '__main__':
    Mendenhall_Characteristicr_Curves_of_Composition()
