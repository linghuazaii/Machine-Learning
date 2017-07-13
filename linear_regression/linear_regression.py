#!/bin/env python
# -*- coding: utf-8 -*-
# This file is auto-generated.Edit it at your own peril.
import csv, sys, math
import matplotlib.pyplot as plt
from decimal import Decimal

def read_csv(file_name):
    data = list()
    f = open(file_name, 'rb')
    reader = csv.reader(f, delimiter = ',')
    for row in reader:
        try:
            x = Decimal(row[0])
            y = Decimal(row[1])
            data.append((x, y))
        except:
            continue
    f.close()
    return data

def draw(data):
    px = [p[0] for p in data]
    py = [p[1] for p in data]
    plt.plot(px, py, 'r.')

def draw_test():
    px = [1,2,2,3,3,4,5,6,6,6,8,10]
    py = [-890,-1411,-1560,-2220,-2091,-2878,-3537,-3268,-3920,-4163,-5471,-5157]
    plt.plot(px, py, 'r.')
    plt.savefig('test.png')
    plt.clf()

def cost(data, fx, k, b):
    cost_val = Decimal(0.0)
    for point in data:
        cost_val += pow(fx(k, b, point[0]) - point[1], 2)
    cost_val /= 2 * len(data)
    return cost_val

# cost(k)'
def derivate_k(data, fx, k, b):
    d = Decimal(0.0)
    for point in data:
        d += fx(k, b, point[0]) - point[1]
    d /= len(data)
    return d

# cost(b)'
def derivate_b(data, fx, k, b):
    d = Decimal(0.0)
    for point in data:
        d += (fx(k, b, point[0]) - point[1]) * point[0]
    d /= len(data)
    return d

def calc_line_function(data, learn_rate):
    '''
        cost = 1/(2m) * E(1->m)(Y(i) - y(i))^2
        Y(i) = k + b * x(i)
        cost(k)' = d(cost)/d(k) = 1/m * E(1->m)(Y(i) - y(i))
        cost(b)' = d(cost)/d(b) = 1/m * E(1->m)((Y(i) - y(i)) * x(i))
        for gradient descent, a means learning rate.
        update k:
            k = k - a * cost(k)'
            b = b - a * cost(b)'
    '''
    k = Decimal(0.0)
    b = Decimal(0.0)
    a = Decimal(learn_rate)
    fx = lambda m, n, x: (m + n * x)
    last_cost = cost(data, fx, k, b)
    while True:
        new_k = k - a * derivate_k(data, fx, k, b)
        new_b = b - a * derivate_b(data, fx, k, b)
        k = new_k
        b = new_b
        new_cost = cost(data, fx, k, b)
        #print "k:%s  b:%s  %s" % (k, b, math.fabs(new_cost - last_cost))
        print "k:%s  b:%s  %s" % (k, b, new_cost)
        if math.fabs(new_cost - last_cost) <= 0.0001:
            return k, b
        last_cost = new_cost

def draw_line(data, k, b):
    min_x = min([p[0] for p in data])
    max_x = max([p[0] for p in data])
    px = [min_x, max_x]
    py = [k + b * x for x in px]
    plt.plot(px, py, 'b', linewidth = 2.0)

def save_image(image, label):
    plt.ylabel(label)
    plt.savefig(image)
    plt.clf()

def main():
    data = read_csv('train.csv')
    k, b = calc_line_function(data, 0.00001)
    draw(data)
    draw_line(data, k, b)
    save_image('train.png', 'train')
    test_data = read_csv('test.csv')
    draw(test_data)
    draw_line(data, k, b)
    save_image('test.png', 'test')

if __name__ == "__main__":
    main()

