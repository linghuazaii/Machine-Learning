#!/bin/env python
# -*- coding: utf-8 -*-
# This file is auto-generated.Edit it at your own peril.
from math import sqrt

def readfile(filename):
    lines = [line for line in file(filename)]
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(i) for i in p[1:]])

    return rownames, colnames, data

def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0:
        return 0

    return 1.0 - num / den

class bicluster:
    def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance = pearson):
    distances = {}
    current_clust_id = -1
    clust = [bicluster(rows[i], id = i) for i in range(len(rows))]
    while len(clust) > 1:
        lowest_pair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                d = distances[(clust[i].id, clust[j].id)]
                if d < closest:
                    closest = d
                    lowest_pair = (i, j)
        mergevec = [(clust[lowest_pair[0]].vec[i] + clust[lowest_pair[1]].vec[i]) / 2.0 for i in range(len(clust[0].vec))]
        new_cluster = bicluster(mergevec, left = clust[lowest_pair[0]], right = clust[lowest_pair[1]], distance = closest, id = current_clust_id)
        current_clust_id  -= 1
        new_clust = [clust[i] for i in range(len(clust)) if i not in (lowest_pair[0], lowest_pair[1])]
        clust = new_clust
        clust.append(new_cluster)
    #print "clust len: %s" % len(clust)
    #print "clust id: %s" % clust[0].id
    return clust[0]

def print_cluster(clust, labels = None, n = 0):
    for i in range(n):
        print ' ',
    if clust.id < 0:
        print '-'
    else:
        if labels == None:
            print clust.id
        else:
            print labels[clust.id]
    if clust.left != None:
        print_cluster(clust.left, labels = labels, n = n + 1)
    if clust.right != None:
        print_cluster(clust.right, labels = labels, n = n + 1)

def create_cluster():
    blognames, words, data = readfile('blogdata.txt')
    clust = hcluster(data)
    print_cluster(clust, labels = blognames)

def main():
    create_cluster()

if __name__ == "__main__":
    main()

