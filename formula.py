# coding=<utf-8>
import numpy as np
import pandas as pd
import os
from math import log as ln
from math import sqrt

def return_on_day_t (P_t, P_before_t):
    "defines the logarith return of the stock over the one date period from (t-1) to t"
    return ln(P_t / P_before_t)

def average_stock_return (returns, n):
    "The average return of the stock over the period of n days"
    # calculate sum of returns
    sum = np.sum(returns)
    # average of returns
    E = sum / n
    return E

def variance (returns, E, n):
    "The variance of the stock over the period of n days"
    sum = 0
    # calculate sum
    for r in returns:
       sum += (r - E) ** 2
    # variance
    var = sum / n
    return var

def average_two_stocks_return (returns1, returns2, n):
    sum = np.sum(map(lambda r1, r2: r1 * r2, returns1, returns2))
    # average of returns
    E = sum / n
    return E

def coeff(E12, E1, E2, var1, var2):
    "Correlation coefficient between 2 stocks"
    cor_coeff = (E12 - E1 * E2) / sqrt(var1 * var2)
    return cor_coeff

def calc_coeff(returns1, returns2, n):
    E1 = average_stock_return(returns1, n)
    E2 = average_stock_return(returns2, n)
    var1 = variance(returns1, E1, n)
    var2 = variance(returns2, E2, n)
    E12 = average_two_stocks_return(returns1, returns2, n)
    return coeff(E12, E1, E2, var1, var2)

def create_returns_list(csv, start, end):
    "create return values list of a stock in range from start to end with data stored in Dataframe csv"
    dates = pd.date_range(start=start, end=end)
    dates = map(lambda x: x.strftime('%Y%m%d'), dates)
    full_price_list = pd.Series(index=dates) # list of prices that contains missing days

    # get prices list in csv
    date_column_name = '<DTYYYYMMDD>'
    price_column_name = '<Close>'
    frame = csv[(csv[date_column_name].astype('string') >= start) & (csv[date_column_name].astype('string') <= end)]  # trim csv
    lack_price_list = pd.Series(data=frame[price_column_name].tolist(), index=frame[date_column_name].tolist())

    # fill out values that already present in lack list into full list
    for date, value in lack_price_list.iteritems():
        full_price_list[str(date)] = value

    # fill out NaN in full list
    # fill first row
    if(np.isnan(full_price_list[0])):
        # If a stock was offered for trading after the beginning of the studied period then
        # the price was considered to be equal to the price fixed on the first day of trading
        for idx, p in full_price_list.iteritems():
            if(~np.isnan(p)):
                full_price_list[0] = p
                break
    # When there were no transactions on a given trading day the price for a stock was considered
    # to be unchanged
    return_list = []
    n = len(full_price_list)
    for i in range(1, n):
        if(np.isnan(full_price_list[i])):
            full_price_list[i] = full_price_list[i - 1]
            return_list.append(0)
        else:
            return_list.append(return_on_day_t(full_price_list[i], full_price_list[i - 1]))

    return return_list

def mean_and_deviation(returns_list):
    "return mean and deviation of correlation coefficient values between stocks"
    n = len(returns_list)
    coeff_list = []
    num_of_day = len(returns_list[0]) # all lists equal in number of days
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            coeff = calc_coeff(returns_list[i], returns_list[j], num_of_day)
            coeff_list.append(coeff)
    mean = np.mean(coeff_list)
    var = np.var(coeff_list)
    dev = sqrt(var)
    return mean,dev

def mean_and_deviation2(returns_list):
    "return mean and deviation of correlation coefficient values between stocks"
    n = len(returns_list)
    coeff_list = []
    num_of_day = len(returns_list[0]) # all lists equal in number of days
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            coeff = calc_coeff(returns_list[i], returns_list[j], num_of_day)
            coeff_list.append(coeff)
    mean = np.mean(coeff_list)
    var = np.var(coeff_list)
    dev = sqrt(var)
    return mean,dev,coeff_list