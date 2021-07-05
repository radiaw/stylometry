#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Common imports
import load_dataset as ld
import numpy as np
import pandas as pd
import numpy.random as rnd
import matplotlib.pyplot as plt
import math
import re

# Load nltk
import nltk
nltk.download('punkt')

"""
Test 3: John Burrows’ Delta Method (Advanced)

Like Kilgariff’s chi-squared, Burrows’ Delta is a measure of the “distance” between
a text whose authorship we want to ascertain and some other corpus. Unlike
chi-squared, however, the Delta Method is designed to compare an anonymous text
(or set of texts) to many different authors’ signatures at the same time. More
precisely, Delta measures how the anonymous text and sets of texts written by an
arbitrary number of known authors all diverge from the average of all of them put
together. Furthermore, the Delta Method gives equal weight to every feature that
it measures, thus avoiding the problem of common words overwhelming the results,
which was an issue with chi-squared tests. For all of these reasons, John Burrows’
Delta Method is usually a more effective solution to the problem of authorship.

Burrows’ original algorithm can be summarized as follows:

    * Assemble a large corpus made up of texts written by an arbitrary number of
      authors; let’s say that number of authors is x.
    * Find the n most frequent words in the corpus to use as features.
    * For each of these n features, calculate the share of each of the x authors’
      subcorpora represented by this feature, as a percentage of the total number
      of words. As an example, the word “the” may represent 4.72% of the words in
      Author A’s subcorpus.
    * Then, calculate the mean and the standard deviation of these x values and use
      them as the offical mean and standard deviation for this feature over the
      whole corpus. In other words, we will be using a mean of means instead of
      calculating a single value representing the share of the entire corpus
      represented by each word. This is because we want to avoid a larger subcorpus,
      like Hamilton’s in our case, over-influencing the results in its favor and
      defining the corpus norm in such a way that everything would be expected to
      look like it.
    * For each of the n features and x subcorpora, calculate a z-score describing
      how far away from the corpus norm the usage of this particular feature in
      this particular subcorpus happens to be. To do this, subtract the “mean of
      means” for the feature from the feature’s frequency in the subcorpus and
      divide the result by the feature’s standard deviation. Figure 7 shows the
      z-score equation for feature ‘i’, where C(i) represents the observed frequency,
      the greek letter mu represents the mean of means, and the greek letter sigma,
      the standard deviation.
    * Then, calculate the same z-scores for each feature in the text for which we
      want to determine authorship.
    * Finally, calculate a delta score comparing the anonymous paper with each
      candidate’s subcorpus. To do this, take the average of the absolute values of
      the differences between the z-scores for each feature between the anonymous
      paper and the candidate’s subcorpus. (Read that twice!) This gives equal
      weight to each feature, no matter how often the words occur in the texts;
      otherwise, the top 3 or 4 features would overwhelm everything else.
    * The “winning” candidate is the author for whom the delta score between the
      author’s subcorpus and the test case is the lowest.

Stefan Evert et al. provide an in-depth discussion of the method’s variants,
refinements and intricacies, but we will stick to the essentials for the purposes of
this lesson. A different explanation of Delta, written in Spanish, and an application
to a corpus of Spanish novels can also be found in a recent paper by José Calvo Tello.

"""
def John_Burrows_Delta_Method():
    # Load dataset
    ld.dataset_load()

    # Who are we dealing with this time?
    authors = ("Jordan", "Sanderson")

    # Transform the authors' corpora into lists of word tokens
    books_by_author_tokens = {}

    # Lowercase the tokens so that the same word, capitalized or not,
    # counts as one word
    regex = r'[^\w\d\s]+'
    subst = ""
    for author in authors:
        books = re.sub(regex, subst, ld.books_by_author[author])
        tokens = nltk.word_tokenize(books)

        # Filter out punctuation
        books_by_author_tokens[author] = (
            [token for token in tokens if any(c.isalpha() for c in token)])

        # Convert papers to lowercase to count all tokens of the same word together
        # regardless of case
        books_by_author_tokens[author] = (
             [token.lower() for token in books_by_author_tokens[author]])

    # Combine every paper except our test case into a single corpus
    whole_corpus = []
    for author in authors:
        whole_corpus += books_by_author_tokens[author]

    # Get a frequency distribution
    whole_corpus_freq_dist = list(nltk.FreqDist(whole_corpus).most_common(n = 300))

    # Print the Feature Frequency Distribution in all books
    print("The Feature Frequency Distribution in all books:\n")
    print("  Index     Feature     Frequency")
    print("---------+----------+---------------")
    for index, (word, count) in enumerate(whole_corpus_freq_dist):
        print("%5d  %10s%s" % (index, word.upper(), '{:15,}'.format(count)))
    print("\n");

    # The main data structure
    features = [word for word,freq in whole_corpus_freq_dist]
    feature_freqs = {}

    for author in authors:
        # A dictionary for each candidate's features
        feature_freqs[author] = {}

        # A helper value containing the number of tokens in the author's subcorpus
        overall = len(books_by_author_tokens[author])

        # Calculate each feature's presence in the subcorpus
        for feature in features:
            presence = books_by_author_tokens[author].count(feature)
            feature_freqs[author][feature] = presence / overall

    # The data structure into which we will be storing the "corpus standard" statistics
    corpus_features = {}

    # For each feature...
    for feature in features:
        # Create a sub-dictionary that will contain the feature's mean
        # and standard deviation
        corpus_features[feature] = {}

        # Calculate the mean of the frequencies expressed in the subcorpora
        feature_average = 0
        for author in authors:
            feature_average += feature_freqs[author][feature]
        feature_average /= len(authors)
        corpus_features[feature]["Mean"] = feature_average

        # Calculate the standard deviation using the basic formula for a sample
        feature_stdev = 0
        for author in authors:
            diff = feature_freqs[author][feature] - corpus_features[feature]["Mean"]
            feature_stdev += diff*diff
        feature_stdev /= (len(authors) - 1)
        feature_stdev = math.sqrt(feature_stdev)
        corpus_features[feature]["StdDev"] = feature_stdev

    feature_zscores = {}
    for author in authors:
        feature_zscores[author] = {}
        for feature in features:

            # Z-score definition = (value - mean) / stddev
            # We use intermediate variables to make the code easier to read
            feature_val = feature_freqs[author][feature]
            feature_mean = corpus_features[feature]["Mean"]
            feature_stdev = corpus_features[feature]["StdDev"]
            feature_zscores[author][feature] = ((feature_val-feature_mean) /
                                                feature_stdev)

    # Tokenize the test case
    testcase_book = re.sub(regex, subst, ld.books_by_author["TestCase"])
    testcase_tokens = nltk.word_tokenize(testcase_book)

    # Filter out punctuation and lowercase the tokens
    testcase_tokens = [token.lower() for token in testcase_tokens
                       if any(c.isalpha() for c in token)]

    # Calculate the test case's features
    overall = len(testcase_tokens)
    testcase_freqs = {}
    for feature in features:
        presence = testcase_tokens.count(feature)
        testcase_freqs[feature] = presence / overall

    # Calculate the test case's feature z-scores
    testcase_zscores = {}
    for index, feature in enumerate(features):
        feature_val = testcase_freqs[feature]
        feature_mean = corpus_features[feature]["Mean"]
        feature_stdev = corpus_features[feature]["StdDev"]
        testcase_zscores[feature] = (feature_val - feature_mean) / feature_stdev
        print("%5d  Test case z-score for feature %10s is %20.16f" %
              (index, feature.upper(), testcase_zscores[feature]))
    print("\n");

    for author in authors:
        delta = 0
        for feature in features:
            delta += math.fabs((testcase_zscores[feature] -
                                feature_zscores[author][feature]))
        delta /= len(features)
        print( "Delta score for candidate", author, "is", delta )
    print("\n");

if __name__ == '__main__':
    John_Burrows_Delta_Method()
