# coding:utf-8
import pandas as pd
import numpy as np
import os

#练习地址：https://www.cnblogs.com/rango-lhl/p/9729334.html
#数据集地址：https://github.com/Rango-2017/Pandas_exercises

'''
#####1.开始了解你的数据
探索Chipotle快餐数据
-- 将数据集存入一个名为chipo的数据框内
-- 查看前10行内容
-- 数据集中有多少个列(columns)？
-- 打印出全部的列名称
-- 数据集的索引是怎样的？
-- 被下单数最多商品(item)是什么?
-- 在item_name这一列中，一共有多少种商品被下单？
-- 在choice_description中，下单次数最多的商品是什么？
-- 一共有多少商品被下单？
-- 将item_price转换为浮点数
-- 在该数据集对应的时期内，收入(revenue)是多少？
-- 在该数据集对应的时期内，一共有多少订单？
-- 每一单(order)对应的平均总价是多少？
'''

# -- 将数据集存入一个名为chipo的数据框内
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))#获取项目根目录
path = os.path.join(PROJECT_ROOT,"Pandas_exercises-master/chipotle.tsv") #文件路径
chipo = pd.read_csv(path,sep='\t')#读取xlsx文件内容
#print (chipo)

# -- 查看前10行内容
print (chipo.head(10))

# -- 数据集中有多少个列(columns)？
#print (chipo.shape[1])
#5

# -- 打印出全部的列名称
print (chipo.columns)
# Index(['order_id', 'quantity', 'item_name', 'choice_description',
#        'item_price'],
#       dtype='object')

# -- 数据集的索引是怎样的？
#print (chipo.index)
#RangeIndex(start=0, stop=4622, step=1)

# -- 被下单数最多商品(item)是什么?
#print (chipo[['item_name','quantity']].groupby(by=['item_name']).sum().sort_values(by=['quantity'],ascending=False))

# -- 在item_name这一列中，一共有多少种商品被下单？
#print (chipo['item_name'].unique().shape[0])
#50

# -- 在choice_description中，下单次数最多的商品是什么？
#print (chipo['choice_description'].value_counts().head())
# [Diet Coke]                                                                          134
# [Coke]                                                                               123
# [Sprite]                                                                              77
# [Fresh Tomato Salsa, [Rice, Black Beans, Cheese, Sour Cream, Lettuce]]                42
# [Fresh Tomato Salsa, [Rice, Black Beans, Cheese, Sour Cream, Guacamole, Lettuce]]     40

# -- 一共有多少商品被下单？
num = chipo['quantity'].sum()
#print (num)

# -- 将item_price转换为浮点数
chipo['item_price'] = chipo['item_price'].apply(lambda x: float(x[1:]))
#print (chipo)

# -- 在该数据集对应的时期内，收入(revenue)是多少？
chipo['revenue'] = chipo['quantity'] * chipo['item_price']
print (chipo['revenue'].sum())

# -- 在该数据集对应的时期内，一共有多少订单？
print (chipo['order_id'].unique().shape[0])

# -- 每一单(order)对应的平均总价是多少？
chipo['item_price_sum'] = chipo['quantity'] * chipo['item_price']
df = chipo[['order_id','item_price_sum']].groupby(by=['order_id']).sum().mean()
print (df)


'''
#####2 - 数据过滤与排序
探索2012欧洲杯数据
-- 将数据集命名为euro12
-- 只选取 Goals 这一列
-- 有多少球队参与了2012欧洲杯？
-- 该数据集中一共有多少列(columns)?
-- 将数据集中的列Team, Yellow Cards和Red Cards单独存为一个名叫discipline的数据框
-- 对数据框discipline按照先Red Cards再Yellow Cards进行排序
-- 计算每个球队拿到的黄牌数的平均值
-- 找到进球数Goals超过6的球队数据
-- 选取以字母G开头的球队数据
-- 选取前7列
-- 选取除了最后3列之外的全部列
-- 找到英格兰(England)、意大利(Italy)和俄罗斯(Russia)的射正率(Shooting Accuracy)
'''



