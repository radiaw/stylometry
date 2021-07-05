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
Test 2: Kilgariff’s Chi-Squared Method

In a 2001 paper, Adam Kilgarriff15 recommends using the chi-squared statistic to
determine authorship. Readers familiar with statistical methods may recall that
chi-squared is sometimes used to test whether a set of observations (say, voters’
intentions as stated in a poll) follow a certain probability distribution or 
pattern. This is not what we are after here. Rather, we will simply use the 
statistic to measure the “distance” between the vocabularies employed in two sets
of texts. The more similar the vocabularies, the likelier it is that the same 
author wrote the texts in both sets. This assumes that a person’s vocabulary and
word usage patterns are relatively constant.

Here is how to apply the statistic for authorship attribution:

    * Take the corpora associated with two authors.
    * Merge them into a single, larger corpus.
    * Count the tokens for each of the words that can be found in this larger corpus.
    * Select the n most common words in the larger corpus.
    * Calculate how many tokens of these n most common words we would have expected
      to find in each of the two original corpora if they had come from the same author.
      This simply means dividing the number of tokens that we have observed in the 
      combined corpus into two values, based on the relative sizes of the two authors’
      contributions to the common corpus.
    * Calculate a chi-squared distance by summing, over the n most common words, the
      squares of the differences between the actual numbers of tokens found in each
      author’s corpus and the expected numbers, divided by the expected numbers.
      Figure 6 shows the equation for the chi-squared statistic, where C(i) represents
      the observed number of tokens for feature ‘i’, and E(i), the expected number for
      this feature.
"""
def Kilgariff_Chi_Squared_Method():
    # Load dataset
    ld.dataset_load()

    authors = ("Hamilton", "Madison", "Disputed")

    # Transform the authors' corpora into lists of word tokens
    federalist_by_author_tokens = {}

    # Lowercase the tokens so that the same word, capitalized or not,
    # counts as one word
    for author in authors:
        tokens = nltk.word_tokenize(ld.federalist_by_author[author])

        # Filter out punctuation
        federalist_by_author_tokens[author] = (
            [token for token in tokens if any(c.isalpha() for c in token)])

        federalist_by_author_tokens[author] = (
             [token.lower() for token in federalist_by_author_tokens[author]])

    # Who are the authors we are analyzing?
    authors = ("Hamilton", "Madison")

    # Calculate chisquared for each of the two candidate authors
    for author in authors:

        # First, build a joint corpus and identify the 500 most frequent words in it
        joint_corpus = (federalist_by_author_tokens[author] +
            federalist_by_author_tokens["Disputed"])
        joint_freq_dist = nltk.FreqDist(joint_corpus)
        most_common = list(joint_freq_dist.most_common(500))

        # What proportion of the joint corpus is made up
        # of the candidate author's tokens?
        author_share = (len(federalist_by_author_tokens[author])
            / len(joint_corpus))

        # Now, let's look at the 500 most common words in the candidate
        # author's corpus and compare the number of times they can be observed
        # to what would be expected if the author's papers
        # and the Disputed papers were both random samples from the same distribution.
        chisquared = 0
        for word,joint_count in most_common:

            # How often do we really see this common word?
            author_count = federalist_by_author_tokens[author].count(word)
            disputed_count = federalist_by_author_tokens["Disputed"].count(word)

            # How often should we see it?
            expected_author_count = joint_count * author_share
            expected_disputed_count = joint_count * (1-author_share)

            # Add the word's contribution to the chi-squared statistic
            chisquared += ((author_count-expected_author_count) *
               (author_count-expected_author_count) /
               expected_author_count)

            chisquared += ((disputed_count-expected_disputed_count) *
               (disputed_count-expected_disputed_count)
               / expected_disputed_count)

        print("The Chi-squared statistic for candidate", author, "is", chisquared)
    print("\n");

if __name__ == '__main__':
    Kilgariff_Chi_Squared_Method()
