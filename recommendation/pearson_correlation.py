#!/bin/env python
# -*- coding: utf-8 -*-
# This file is auto-generated.Edit it at your own peril.
from common import *
from math import sqrt

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def calc_covaration(person1, person2):
    # cov(x, y) = E(xy) - E(x)E(y)
    movies = extract_keys(person1, person2)
    mean1 = 0.0
    mean2 = 0.0
    mean1_2 = 0.0
    for movie in movies:
        mean1 += person1.get(movie, 1)
        mean2 += person2.get(movie, 1)
        mean1_2 += person1.get(movie, 1) * person2.get(movie, 1)
    mean1 = mean1 / len(movies)
    mean2 = mean2 / len(movies)
    mean1_2 = mean1_2 / len(movies)
    covaration = mean1_2 - mean1 * mean2
    return covaration

def calc_standard_deviation(person1, person2):
    # sd(x) = sqrt(E(x^2) - E(x)^2)
    movies = extract_keys(person1, person2)
    mean1 = 0.0
    mean1_2 = 0.0
    mean2 = 0.0
    mean2_2 = 0.0
    for movie in movies:
        mean1 += person1.get(movie, 1)
        mean1_2 += pow(person1.get(movie, 1), 2)
        mean2 += person2.get(movie, 1)
        mean2_2 += pow(person2.get(movie, 1), 2)
    mean1 /= len(movies)
    mean1_2 /= len(movies)
    mean2 /= len(movies)
    mean2_2 /= len(movies)
    sd1 = sqrt(mean1_2 - pow(mean1, 2))
    sd2 = sqrt(mean2_2 - pow(mean2, 2))
    sd1_2 = sd1 * sd2
    return sd1_2

def calc_pearson_score(person1, person2):
    # pearson(x, y) = cov(x, y) / (sd(x) * sd(y))
    pearson_score = calc_covaration(person1, person2) / calc_standard_deviation(person1, person2)
    return pearson_score

def create_sim_map(data):
    users = extract_keys(critics)
    sim_map = dict()
    for user in users:
        sim_map[user] = dict()

    for user1 in users:
        for user2 in users:
            if user1 != user2:
                sim_score = calc_pearson_score(data[user1], data[user2])
                sim_map[user1][user2] = sim_score
    return sim_map

def main():
    print_dict(critics)
    sim_map = create_sim_map(critics)
    print_dict(sim_map)

if __name__ == "__main__":
    main()

