#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------
# @brief    get pearson distance.
# 
# @author   d0evi1
# @date     2014.10.17
#------------------------------------

from math import sqrt


#---------------------------------
# @param list1:     input list1
# @param list2:     input list2
# @param n:         list len. list1 and list2 must the same.
#---------------------------------
def get_pearson(list1, list2, n):
    val = 0
    
    sum1 = sum(list1)
    sum2 = sum(list2)

    sum1Sqrt = sum([ pow(i, 2) for i in list1 ])
    sum2Sqrt = sum([ pow(i, 2) for i in list2 ])

    sumXY = 0
    for i in range(n):
        sumXY += list1[i] * list2[i]

    num = sumXY - (sum1 * sum2 / n)
    den = sqrt((sum1Sqrt - pow(sum1, 2) / n) * (sum2Sqrt - pow(sum2, 2)/n))
    if den == 0:
        return 0

    return num/den

#---------------------------
# main
#---------------------------
if __name__ == '__main__':
    list1 = [32129, 323, 32123, 32093, 144, 872, 1098, 21992, 1290, 89198]
    list2 = [32120, 320, 32110, 32090, 140, 870, 1100, 21980, 1280, 89190]

    print len(list1)
    print get_pearson(list1, list2, len(list1))


