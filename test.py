# coding:utf-8
import pandas as pd
import numpy as np
import os
import random

dic = {}
str = '黑化肥发灰会挥发，灰化肥挥发会发黑'
for i in str:
    print (i)
    if i in dic:
        dic[i]+=1
        # n = dic[i] + 1
        # dic[i] = n
    else:
        dic[i] = 1
print (dic)



