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
    #'Jordan': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'Jordan': [1, 2, 3, 4, 5, 7, 8, 9, 10, 11],
    'Sanderson': [12, 13, 14],
    'TestCase': [1],
}

# Make a dictionary out of the authors' corpora
books_by_author = {}

# A function that compiles all of the text files associated with a single author into a single string
def read_files_into_string(author, filenames):
    strings = []
    for filename in filenames:
        with open(f'data/{author}_{str(filename).zfill(2)}.txt') as f:
            strings.append(f.read())
    return '\n'.join(strings)


def dataset_load():
    for author, files in papers.items():
        books_by_author[author] = read_files_into_string(author, files)

    for author in papers:
        print("\n======>>>   Author: %s,  book size: %s bytes\n" % (author, '{:,}'.format(len(books_by_author[author]))))
        print(books_by_author[author][:100])
        print("\n")

if __name__ == '__main__':
    dataset_load()
