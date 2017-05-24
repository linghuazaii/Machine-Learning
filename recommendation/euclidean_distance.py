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

def calc_sim_score(person1, person2):
    movies = extract_keys(person1, person2)
    score = 0
    for movie in movies:
        score_p1 = person1.get(movie, 0)
        score_p2 = person2.get(movie, 0)
        score += pow((score_p1 - score_p2), 2)
    distance = 1.0 / (1 + sqrt(score))

    return distance

def create_sim_map(data):
    users = extract_keys(critics)
    sim_map = dict()
    for user in users:
        sim_map[user] = dict()

    for user1 in users:
        for user2 in users:
            if user1 != user2:
                sim_score = calc_sim_score(data[user1], data[user2])
                sim_map[user1][user2] = sim_score

    return sim_map   


def main():
    #print_dict(critics)
    sim_map = create_sim_map(critics)
    print_dict(sim_map)


if __name__ == "__main__":
    main()

