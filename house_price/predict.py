#!/bin/env python
# -*- coding: utf-8 -*-
# This file is auto-generated.Edit it at your own peril.
import pandas, datetime, time, numpy
from matplotlib import pyplot as plt

def read_csv(path):
    data = pandas.read_csv(path).to_dict()
    for key, value in data.iteritems():
        vals = list()
        for k, v in value.iteritems():
            vals.append(v)
        data[key] = vals
    return data

def get_timestamp(date):
    date = date[0:8]
    timestamp = time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple())
    return timestamp

def plot_date(data):
    py = data['price']
    px = [get_timestamp(date) for date in data['date']]
    plt.plot([numpy.log(x) for x in px], [numpy.log(y) for y in py], 'r.')
    plt.ylabel('Price/Date')
    plt.savefig('price-date_transform.png')
    plt.clf()
    
def plot_bedrooms(data):
    py = data['price']
    px = data['bedrooms']
    #plt.plot([numpy.log(x) for x in px], [numpy.log(y) for y in py], 'r.')
    plt.plot(px, [numpy.log(y) for y in py], 'r.')
    plt.ylabel('Price/Bedrooms')
    plt.savefig('price-bedrooms_transform.png')
    plt.clf()

def main():
    data = read_csv('kc_house_data.csv')
    #plot_date(data)
    plot_bedrooms(data)

if __name__ == "__main__":
    main()

