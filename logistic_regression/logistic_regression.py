#!/bin/env python
# -*- coding: utf-8 -*-
# This file is auto-generated.Edit it at your own peril.
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

def load_data(data_file):
    data = np.loadtxt(open(data_file, 'rb'), delimiter = ',', skiprows = 1, usecols = (1,2,3))
    X = data[:, 0:2]
    X = np.append(X, np.reshape(X[:,0] * X[:,1], (X.shape[0], 1)), axis = 1)
    Y = data[:, 2]
    Y = np.reshape(Y, (Y.shape[0], 1))
    return X, Y

def plot_data(X, Y, image):
    positive = np.where(Y == 1)
    negative = np.where(Y == 0)
    #plt.plot(X[positive,0], X[positive, 1], 'ro', label = 'positive')
    #plt.plot(X[negative, 0], X[negative, 1], 'gx', label = 'negative')
    plt.scatter(X[positive,0], X[positive, 1], marker = 'o', c = 'r')
    plt.scatter(X[negative, 0], X[negative, 1], marker = 'o', c = 'g')
    plt.xlabel('grade1')
    plt.ylabel('grade2')
    plt.legend(['positive', 'negative'])
    #plt.savefig(image)
    #plt.clf()

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def cost(theta, x, y, lam = 0.):
    m = x.shape[0]
    theta = np.reshape(theta, (len(theta), 1))
    lamb = theta
    lamb[0][0] = 0.
    J = (-1.0 / m) * (y.T.dot(np.log(sigmoid(x.dot(theta)))) + (1 - y).T.dot(np.log(1 - sigmoid(x.dot(theta))))) + lam / (2 * m) * lamb.T.dot(lamb)
    #grad = (1.0 ./ m) * (np.transpose(x).dot(sigmoid(x.dot(theta) - y))) + (lam / m) * lamb
    #print J
    return J[0][0]

def grad(theta, x, y, lam = 0.):
    m = x.shape[0]
    theta = np.reshape(theta, (len(theta), 1))
    lamb = theta
    lamb[0][0] = 0.
    grad = (1.0 / m) * (x.T.dot(sigmoid(x.dot(theta) - y))) + (lam / m) * lamb
    grad = grad.flatten()
    return grad

def plot_boundary(theta):
    x1 = np.arange(-1.0, 1.0, 0.001)
    x2 = -(theta[0] + theta[1] * x1) / (theta[2] + theta[3] * x1)
    plt.plot(x1, x2)
    plt.savefig('boundary01.png')
    plt.clf()

def main():
    X, Y = load_data('data.csv')
    plot_data(X, Y, 'data.png')

    #theta = np.random.randn(4)
    theta = [-3.87155337e-04, -5.70516730e-01, -1.05983874e+00, -4.53414382e-01]
    #print theta
    X_new = np.append(np.ones((X.shape[0], 1)), X, axis = 1)
    theta_final = opt.fmin_tnc(cost, theta, fprime = grad, args = (X_new, Y))
    theta_final = theta_final[0]
    print theta_final
    plot_boundary(theta_final)


if __name__ == "__main__":
    main()

