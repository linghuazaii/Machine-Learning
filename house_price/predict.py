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

def deviation_score(x, data):
    return (x - numpy.mean(data)) / numpy.std(data, ddof = 1)

def plot_date(data):
    py = data['price']
    px = [get_timestamp(date) for date in data['date']]
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/Date')
    plt.savefig('price-date.png')
    plt.clf()
    
def plot_bedrooms(data):
    py = data['price']
    px = data['bedrooms']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/Bedrooms')
    plt.savefig('price-bedrooms.png')
    plt.clf()

def plot_bathrooms(data):
    py = data['price']
    px = data['bathrooms']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/Bathrooms')
    plt.savefig('price-bathrooms.png')
    plt.clf()

def plot_sqft_living(data):
    py = data['price']
    px = data['sqft_living']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/sqft_living')
    plt.savefig('price-sqft_living.png')
    plt.clf()

def plot_sqft_lot(data):
    py = data['price']
    px = data['sqft_lot']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/sqft_lot')
    plt.savefig('price-sqft_lot.png')
    plt.clf()

def plot_floors(data):
    py = data['price']
    px = data['floors']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/Floors')
    plt.savefig('price-floors.png')
    plt.clf()

def plot_waterfront(data):
    py = data['price']
    px = data['waterfront']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/Waterfront')
    plt.savefig('price-waterfront.png')
    plt.clf()

def plot_view(data):
    py = data['price']
    px = data['view']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/View')
    plt.savefig('price-view.png')
    plt.clf()

def plot_condition(data):
    py = data['price']
    px = data['condition']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/Condition')
    plt.savefig('price-condition.png')
    plt.clf()

def plot_grade(data):
    py = data['price']
    px = data['grade']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/Grade')
    plt.savefig('price-grade.png')
    plt.clf()

def plot_sqft_above(data):
    py = data['price']
    px = data['sqft_above']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/Sqft_above')
    plt.savefig('price-sqft_above.png')
    plt.clf()

def plot_sqft_basement(data):
    py = data['price']
    px = data['sqft_basement']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/sqft_basement')
    plt.savefig('price-sqft_basement.png')
    plt.clf()

def plot_yr_built(data):
    py = data['price']
    px = data['yr_built']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/yr_built')
    plt.savefig('price-yr_built.png')
    plt.clf()

def plot_yr_renovated(data):
    py = data['price']
    px = data['yr_renovated']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/yr_renovated')
    plt.savefig('price-yr_renovated.png')
    plt.clf()

def plot_zipcode(data):
    py = data['price']
    px = data['zipcode']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/zipcode')
    plt.savefig('price-zipcode.png')
    plt.clf()

def plot_lat(data):
    py = data['price']
    px = data['lat']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/lat')
    plt.savefig('price-lat.png')
    plt.clf()

def plot_long(data):
    py = data['price']
    px = data['long']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/long')
    plt.savefig('price-long.png')
    plt.clf()

def plot_sqft_living15(data):
    py = data['price']
    px = data['sqft_living15']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/sqft_living15')
    plt.savefig('price-sqft_living15.png')
    plt.clf()

def plot_sqft_lot15(data):
    py = data['price']
    px = data['sqft_lot15']
    mean_px = numpy.mean(px)
    std_px = numpy.std(px)
    fx = lambda x : (x - mean_px) / std_px
    plt.plot([fx(x) for x in px], py, 'r.')
    plt.ylabel('Price/sqft_lot15')
    plt.savefig('price-sqft_lot15.png')
    plt.clf()

def main():
    data = read_csv('kc_house_data.csv')
    #plot_date(data)
    #plot_bedrooms(data)
    #plot_bathrooms(data)
    #plot_sqft_living(data)
    #plot_sqft_lot(data)
    #plot_floors(data)
    #plot_waterfront(data)
    #plot_view(data)
    #plot_condition(data)
    #plot_grade(data)
    #plot_sqft_above(data)
    #plot_sqft_basement(data)
    #plot_yr_built(data)
    #plot_yr_renovated(data)
    #plot_zipcode(data)
    #plot_lat(data)
    #plot_long(data)
    #plot_sqft_living15(data)
    plot_sqft_lot15(data)


if __name__ == "__main__":
    main()

