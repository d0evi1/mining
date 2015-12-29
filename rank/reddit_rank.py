#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sqrt

#-----------------------------
# reddit use wilson .
#-----------------------------
def _confidence(ups, downs):
    n = ups + downs
    if n == 0:
        return 0

    z = 1.0 #1.0 = 85%, 1.6 = 95%
    phat = float(ups) / n
    return (phat+z*z/(2*n)-z*sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)


#---------------------------
# api
#---------------------------
def confidence(ups, downs):
    if ups + downs == 0:
        return 0
    else:
        return _confidence(ups, downs)

print confidence(9, 1)
print confidence(100,1)
print confidence(100, 0)
