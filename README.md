# stylometry

## Purpose

- Analyze texts using a dataset from multiple authors to determine most likely author of the test case through stylometry (process of analyzing authors' writing styles using computational methods)
- Idea from AP English Lang exam reading passage
- Stylometric.py: Wanted to compare Robert Jordan's and Brandon Sanderson's writing styles, because Sanderson had to take over for Jordan's Wheel of Time series. I wanted to see if their writing styles were similar, because if different prose styles may be jarring to fans of the series, then Sanderson's style must be at least somewhat similar to Jordan's
    - Returns a list of 300 most frequently occurring words (Features) in dataset and then z-score value calculations for each feature; finally calculate a delta score for each author in the dataset - lowest delta value = most likely author
- word_freq.py: found a list of 50 most frequently appearing words in a book on the database website, wanted to see if I got similar results

## Algorithm(s)

- John Burrow's Delta Method, a "measure of the "distance” between a text whose authorship we want to ascertain and some other corpus . . . the Delta Method is designed to compare an anonymous text (or set of texts) to many different authors’ signatures at the same time. More precisely, Delta measures how the anonymous text and sets of texts written by an arbitrary number of known authors all diverge from the average of all of them put together" (François Dominic Laramée); smallest value of divergence = most likely author
- Natural Language Toolkit (NLTK):
    - stopwords (filters out common english words such as "that" or "is" or "didn't")
    - tokenize (splits strings into substrings, i.e. words and punctuation)
    - FreqDist class (calculates frequencies of words occurring in each file)
- Regular Expressions (filtered out punctuation: commas, periods, apostrophes, dashes, hyphens, etc.)

## Problems/Bugs Fixed

1. Optimization of word features:
    - Apostrophes in contractions like in "didn't" or "hadn't" caused tokenize() to split the words up into 'didn' and 't' or 'hadn' and 't', creating senseless single-letter "words." Using regular expression re.sub() to substitute such punctuation with empty strings "" solved this problem, turning didn't into didnt and hadn't into hadnt, more manageable for accurate calculations
    - Dashes and hyphens: realized entirely different words were getting concatenated due to dashes/hyphens in between —> because of their different lengths, all occurrences of both - and — had to be replaced using regular expressions, by " " to separate the words affected and improve calculation accuracy
2. Accuracy of delta calculations: adding more variety and quantity of texts as well as multiple authors dropped the delta values from in the 5-6 range to 3-4, then down to 0-1 range

## Datasets

Wheel of Time Series (Robert Jordan (books 1-5, 7-11) and Brandon Sanderson (books 12-14))

Mistborn Trilogy (Brandon Sanderson)

First Law Trilogy (Joe Abercrombie)

Circe (Madeline Miller)

Complete works of Charles Dickens (Charles Dickens (61 pieces + adaptations))

## Tests

- Compare Brandon Sanderson's Mistborn Book 1 as a TestCase_01 against dataset of Robert Jordan's and Brandon Sanderson's Wheel of Time series
    1. Delta values before optimization: 7.09 (Jordan) vs 6.76 (Sanderson)
    2. After: 6.87 vs 6.45
    3. After expansion of dataset: 1.27 vs 0.92; Abercrombie at 1.22, rest authors 1.55+

- Compare Jordan's Wheel of Time Book 6 (TestCase_04) to dataset of Jordan's + Sanderson's Wheel of Time (excluding book 6)
    1. Before optimization: 5.26 (Jordan) vs 6.09 (Sanderson)
    2. After: 3.33 vs 4.07
    3. After expansion of dataset (now comparing against Dickens', Abercrombie's and Miller's works): 0.39 vs 0.93; rest authors 1.22+

- Compare Joe Abercrombie's First Law trilogy (TestCase_05) to itself + entire dataset
    1. Delta value of 0.0 for Joe Abercrombie, as expected

- Compare Charles Dickens' Tale of Two Cities (TestCase_06) to dataset of Wheel of Time, First Law Trilogy, Circe, and Dickens' Complete works (excluding Tale of Two Cities)
    1. Delta value of 0.67 for Dickens; 1.20+ values for the other four authors

## Conclusions/Observations

- Adding multiple authors improved accuracy, dropping delta values from 6-7's to 3-4 range and finally 0-1.5
- In Sanderson's Mistborn test case, the delta values for both Sanderson and Jordan are higher than for Jordan's test case, perhaps due to Jordan's dataset being larger than Sanderson's
- In terms of writing style, Abercrombie seems to be more similar to Sanderson than Jordan, but Sanderson is the most similar to Jordan
- Charles Dickens with his older style of writing is very different from the rest of the modern-day authors, and this is reflected in the delta values for all of them

## Takeaways

- Python Programming
- How to use NLTK library for Nature Language Processing
- How to use Regular Expressions
- How to use GitHub and commit code updates to the cloud
- Linux Terminal commands and vim commands

## Github Link

[https://github.com/radiaw/stylometry](https://github.com/radiaw/stylometry)

## References

1. [https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python](https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python)


2.[https://s3.us-west-2.amazonaws.com/secure.notion-static.com/9ff8592b-40c6-484b-8e55-3081516fa3ff/Understanding_and_explaining_Delta_measures_for_authorship_attribution_2017.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20211013%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211013T223148Z&X-Amz-Expires=86400&X-Amz-Signature=27ac497817257046f8d9a6ee9d070f8e18172c95d8a74039d97a582df49f8e17&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Understanding_and_explaining_Delta_measures_for_authorship_attribution_2017.pdf%22)]
