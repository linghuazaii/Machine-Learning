#!/bin/env python
# -*- coding: utf-8 -*-
# This file is auto-generated.Edit it at your own peril.
import feedparser
import re, sys

reload(sys)
sys.setdefaultencoding('utf-8')

def get_words(html):
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    return [word.lower() for word in words if word != '']

def get_word_count(url):
    doc = feedparser.parse(url)
    #print doc
    wc = {}

    for e in doc.entries:
        if 'summary' in e: 
            summary = e.summary
        else:
            summary = e.description
        words = get_words(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return doc.feed.title, wc

def create_word_vector():
    apcount = {}
    word_counts = {}
    for feedurl in file('feedlist.txt'):
        try:
            title, wc = get_word_count(feedurl)
            word_counts[title] = wc
            for word, count in wc.items():
                apcount.setdefault(word, 0)
                if count > 1:
                    apcount[word] += 1
        except Exception as e:
            print "failed for feed %s" % feedurl
            continue
    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc) / len(word_counts)
        if frac > 0.1 and frac < 0.5:
            wordlist.append(w)

    out = file('blogdata.txt', 'w+')
    out.write('Blog')
    for word in wordlist:
        out.write('\t%s ' % word)
    out.write("\n")
    for blog, wc in word_counts.items():
        out.write(blog)
        for word in wordlist:
            if word in wc:
                out.write("\t%d" % wc[word])
            else:
                out.write('\t0')
        out.write('\n')

def main():
    create_word_vector()

if __name__ == "__main__":
    main()

