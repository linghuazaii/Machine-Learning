#!/bin/env python
# -*- coding: utf-8 -*-
# This file is auto-generated.Edit it at your own peril.
import time, random, math

people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]

destination = 'LGA'

flights = {}

for line in file('schedule.txt'):
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])
    flights[(origin,dest)].append((depart, arrive, int(price)))

def get_minutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]

def print_schedule(r):
    for d in range(len(r) / 2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][r[d]]
        ret = flights[(destination, origin)][r[d + 1]]
        print '%10s|%4s | %5s-%5s $%3s | %5s-%5s $%3s' % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2]) 

def schedule_cost(sol):
    total_price = 0
    latest_arrival = 0
    earliest_dep = 24 * 60

    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]
        total_price += outbound[2]
        total_price += returnf[2]
        if latest_arrival < get_minutes(outbound[1]):
            latest_arrival = get_minutes(outbound[1])
        if earliest_dep > get_minutes(returnf[0]):
            earliest_dep = get_minutes(returnf[0])

    total_wait = 0
    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]
        total_wait += latest_arrival - get_minutes(outbound[1])
        total_wait += get_minutes(returnf[0]) - earliest_dep

    if latest_arrival > earliest_dep:
        total_price += 50

    return total_price + total_wait

def random_optimize(domain, costf):
    best = 9999999999
    bestr = None
    for i in range(10000):
        r = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        cost = costf(r)
        if cost < best:
            best = cost
            bestr = r
    return r

def hill_climb(domain, costf):
    sol = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

    while True:
        neighbors = []
        for j in range(len(domain)):
            if sol[j] > domain[j][0]:
                neighbors.append(sol[0:j] + [sol[j] + 1] + sol[j + 1:])
            if sol[j] < domain[j][0]:
                neightbors.append(sol[0:j] + [sol[j] - 1] + sol[j + 1:])
        current = costf(sol)
        best = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            if cost < best:
                best = cost
                sol = neighbors[j]
        if best == current:
            break;

    return sol

def annealing_optimize(domain, costf, T = 1000000.0, cool = 0.99, step = 1):
    vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

    while T > 0.1:
        i = random.randint(0, len(domain) - 1)
        direction = random.randint(-step, step)
        vecb = vec[:]
        vecb[i] += direction
        if vecb[i] < domain[i][0]:
            vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]:
            vecb[i] = domain[i][1]

        ea = costf(vec)
        eb = costf(vecb)
        p = pow(math.e, float(-eb-ea) / T)
        if (eb < ea or random.random() < p):
            vec = vecb

        T = T * cool
    return vec

def genetic_optimization(domain, costf, popsize = 50, step = 1, mutprob = 0.2, elite = 0.2, max_iter = 100):
    def mutate(vec):
        i = random.randint(0, len(domain) - 1)
        if random.random() < 0.5 and vec[i] > domain[i][0]:
            return vec[0:i] + [vec[i] - step] + vec[i + 1:]
        elif vec[i] < domain[i][1]:
            return vec[0:i] + [vec[i] + step] + vec[i + 1:]
        else:
            return vec

    def cross_over(r1, r2):
        i = random.randint(1, len(domain) - 2)
        return r1[0:i] + r2[i:]

    pop = []
    for i in range(popsize):
        vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        pop.append(vec)

    top_elite = int(elite * popsize)
    for i in range(max_iter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        ranked = [v for (s, v) in scores]
        pop = ranked[0:top_elite]

        while len(pop) < popsize:
            if random.random() < mutprob:
                c = random.randint(0, top_elite)
                pop.append(mutate(ranked[c]))
            else:
                c1 = random.randint(0, top_elite)
                c2 = random.randint(0, top_elite)
                pop.append(cross_over(ranked[c1], ranked[c2]))
        #print scores[0][0]

    return scores[0][1]

def main():
    domain = [(0,8)] * (len(people) * 2)
    #s = random_optimize(domain, schedule_cost)
    #s = hill_climb(domain, schedule_cost)
    #s = annealing_optimize(domain, schedule_cost)
    s = genetic_optimization(domain, schedule_cost)
    print s
    print_schedule(s)
    print schedule_cost(s)

if __name__ == "__main__":
    main()

