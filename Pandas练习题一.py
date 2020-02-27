# coding:utf-8
import pandas as pd
import numpy as np
import os


#1.list或numpy array或dict转pd.Series
print ('-'*10+'1'+'-'*10)

mylist = list('abcedfghijklmnopqrstuvwxyz')
myarr = np.arange(26)

mydic = dict(zip(mylist,myarr))
print (mydic)

ser1 = pd.Series(mylist)
ser2 = pd.Series(myarr)
ser3 = pd.Series(mydic)
print (ser3)

#2.series的index转dataframe的column
print ('-'*10+'2'+'-'*10)

df = ser3.to_frame().reset_index()
print (df)

#3.多个series合并成一个dataframe
print ('-'*10+'3'+'-'*10)

df = pd.DataFrame({'col1': ser1, 'col2': ser2})
print (df)

#4.根据index, 多个series合并成dataframe
print ('-'*10+'4'+'-'*10)

s1 = ser1[:16]
print (s1)
s2 = ser2[14:]
print (s2)
#concat会根据index拼接上
s3 = pd.concat([s1,s2],axis=1)
print (s3)

#5.头尾拼接两个series
print ('-'*20+'5')

print (pd.concat([s1,s2],axis=0))

#6.找到元素 在series A中不在series B中
print ('-'*20+'6')

ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])
print (ser1[~ser1.isin(ser2)])

#7.两个seiries的并集:union1d
print ('-'*20+'7')
ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])
print (np.union1d(ser1,ser2))





# print ('-'*20+'6')
# print ('-'*20+'6')
# print ('-'*20+'6')
# print ('-'*20+'6')
# print ('-'*20+'6')
# print ('-'*20+'6')
# print ('-'*20+'6')
# print ('-'*20+'6')
# print ('-'*20+'6')
# print ('-'*20+'6')
# print ('-'*20+'6')
