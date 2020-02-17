# coding:utf-8
import pandas as pd
import numpy as np
import os
import openpyxl

'''
#读取文件（项目中文件）
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))#获取项目根目录
path = os.path.join(PROJECT_ROOT,"02-13多人讨论围观明细.xlsx") #文件路径

print ('------')
grouped = df.groupby(['sku','课程标题'])
array = np.array()
for sku,group in grouped:
    print (sku[0],sku[1],group.shape[0])
    array.append
'''

#-------数据分组-------#

'''
groupby：
obj.groupby('key')
obj.groupby(['key1','key2'])
obj.groupby(key,axis=1)
'''

'''

#以sku聚合分组
grouped = df.groupby('sku')

#grouped.first()为每一组的第一行数据
print (grouped.first())

print ('****************')

#查看对应分组
print (grouped.groups)

print ('----------------')

#遍历分组
for sku,group in grouped:
    print (sku)
    print (group)
    print (group.shape[0],group.shape[1])#获得每个分组的列的数量

print ('+++++++++++++++++')

#使用get_group（）方法，我们可以选择一个组。
group = grouped.get_group('yxs')
print (group)
print (grouped['用户评分'].mean())

print ('^^^^^^^^^^^^^^^^^^^^')

#Aggregations（聚合）
print (grouped['用户评分'].agg(np.mean))
print (grouped['用户评分'].agg([np.sum,np.mean,np.std]))

'''

#-------筛选数据-------#

'''

#筛选出评分小于等于0.5的评论
bad = df[df['用户评分']<=0.5]
print (bad[:10])#输出前10条

#查看各个sku的数量
sku_count = bad['sku'].value_counts()
print (sku_count)

#查看所有的内容中sku的数量
total_sku_count = df['sku'].value_counts()
print (total_sku_count)

#计算评分小于等于0.5的占总体的百分比
per = sku_count / total_sku_count
print (per)

'''





