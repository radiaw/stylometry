#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Common imports
import os
import argparse
import sys
import platform
import time
import datetime

papers = {
    'Madison': [10, 14, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],
    'Hamilton': [1, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 21, 22, 23, 24,
                 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 59, 60,
                 61, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
                 78, 79, 80, 81, 82, 83, 84, 85],
    'Jay': [2, 3, 4, 5],
    'Shared': [18, 19, 20],
    'Disputed': [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 62, 63],
    'TestCase': [64]
}

# Make a dictionary out of the authors' corpora
federalist_by_author = {}

# A function that compiles all of the text files associated with a single author into a single string
def read_files_into_string(filenames):
    strings = []
    for filename in filenames:
        with open(f'data/federalist_{filename}.txt') as f:
            strings.append(f.read())
    return '\n'.join(strings)


def dataset_load():
    for author, files in papers.items():
        federalist_by_author[author] = read_files_into_string(files)

    for author in papers:
        print(federalist_by_author[author][:100])
    print("\n")

if __name__ == '__main__':
    dataset_load()
