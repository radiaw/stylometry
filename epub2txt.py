#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Common imports
import os
import argparse
import sys
import platform
import time
import datetime
import ebooklib
from ebooklib import epub

def epub_2_txt():
    book = epub.read_epub('Brandon_Sanderson.epub')
    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        print(doc.content)
        #print(doc)

if __name__ == '__main__':
    epub_2_txt()
