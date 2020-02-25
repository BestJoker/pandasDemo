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
#print (chipo.head(10))

# -- 数据集中有多少个列(columns)？
#print (chipo.shape[1])
#5

# -- 打印出全部的列名称
#print (chipo.columns)
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
#print (chipo['revenue'].sum())

# -- 在该数据集对应的时期内，一共有多少订单？
#print (chipo['order_id'].unique().shape[0])

# -- 每一单(order)对应的平均总价是多少？
chipo['item_price_sum'] = chipo['quantity'] * chipo['item_price']
df = chipo[['order_id','item_price_sum']].groupby(by=['order_id']).sum().mean()
#print (df)

print ('----------------------------------')

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

# -- 将数据集命名为euro12
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))#获取项目根目录
path = os.path.join(PROJECT_ROOT,"Pandas_exercises-master/Euro2012.csv") #文件路径
euro12 = pd.read_csv(path)
#print (euro12)
#print (euro12.columns)

# -- 只选取 Goals 这一列
#print (euro12.Goals)

# -- 有多少球队参与了2012欧洲杯？
#print (euro12['Team'].unique())

# -- 该数据集中一共有多少列(columns)?
#print (euro12.shape[1])

# -- 将数据集中的列Team, Yellow Cards和Red Cards单独存为一个名叫discipline的数据框
discipline = euro12[['Team','Yellow Cards','Red Cards']]
#print (discipline)

# -- 对数据框discipline按照先Red Cards再Yellow Cards进行排序
#print (discipline.sort_values(by=['Red Cards','Yellow Cards'],ascending=False))

# -- 计算每个球队拿到的黄牌数的平均值
yellow_cards_mean = discipline.groupby(by=['Yellow Cards']).sum().mean()
#print (yellow_cards_mean)

# -- 找到进球数Goals超过6的球队数据
df = euro12[euro12['Goals'] > 6]
#print (df)

# -- 选取以字母G开头的球队数据
df = euro12[euro12['Team'].str.startswith('G')]
#print (df)

# -- 选取前7列
#print (euro12.iloc[:,0:7])

# -- 选取除了最后3列之外的全部列
#print (euro12[:,0:-3])

# -- 找到英格兰(England)、意大利(Italy)和俄罗斯(Russia)的射正率(Shooting Accuracy)
df = euro12[euro12['Team'].isin(['England','Italy','Russia'])][['Team','Shooting Accuracy']]
#print (df)
#print (euro12.loc[euro12['Team'].isin(['England','Italy','Russia']),['Team','Shooting Accuracy']])

print ('----------------------------------')

'''
#####练习3-数据分组

探索酒类消费数据
-- 将数据框命名为drinks
-- 哪个大陆(continent)平均消耗的啤酒(beer)更多？
-- 打印出每个大陆(continent)的红酒消耗(wine_servings)的描述性统计值
-- 打印出每个大陆每种酒类别的消耗平均值
-- 打印出每个大陆每种酒类别的消耗中位数
-- 打印出每个大陆对spirit饮品消耗的平均值，最大值和最小值
'''

# -- 将数据框命名为drinks
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(PROJECT_ROOT,'Pandas_exercises-master/drinks.csv')
drinks = pd.read_csv(path)
print (drinks)

# -- 哪个大陆(continent)平均消耗的啤酒(beer)更多？
df = drinks[['continent','beer_servings']].groupby(by=['continent']).mean().sort_values(by=['beer_servings'],ascending=False)
#print (df.head(1))

# -- 打印出每个大陆(continent)的红酒消耗(wine_servings)的描述性统计值
#print (drinks.groupby(by=['continent']).wine_servings.describe())


# -- 打印出每个大陆每种酒类别的消耗平均值
#print (drinks.groupby(by=['continent']).mean())

# -- 打印出每个大陆每种酒类别的消耗中位数
#print (drinks.groupby(by=['continent']).median())

# -- 打印出每个大陆对spirit饮品消耗的平均值，最大值和最小值
#print (drinks.groupby(by=['continent']).spirit_servings.describe())


'''
#####练习4-Apply函数
探索1960 - 2014 美国犯罪数据
-- 将数据框命名为crime
-- 每一列(column)的数据类型是什么样的？
-- 将Year的数据类型转换为 datetime64
-- 将列Year设置为数据框的索引
-- 删除名为Total的列
-- 按照Year（每十年）对数据框进行分组并求和
-- 何时是美国历史上生存最危险的年代？
'''

# -- 将数据框命名为crime
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(PROJECT_ROOT,'Pandas_exercises-master/US_Crime_Rates_1960_2014.csv')
crime = pd.read_csv(path)

print (crime.head(15))
print (crime.columns)

# -- 每一列(column)的数据类型是什么样的？
print (crime.info())

# -- 将Year的数据类型转换为 datetime64
crime.Year = pd.to_datetime(crime['Year'],format='%Y')
print (df)

# -- 将列Year设置为数据框的索引
crime = crime.set_index('Year',drop=True)
print (crime)

# -- 删除名为Total的列
del crime['Total']
print (crime.info())

# -- 按照Year（每十年）对数据框进行分组并求和
crimes = crime.resample('10AS').sum()
population = crime.resample('10AS').max()
crimes['Population'] = population
print (crimes)

# -- 何时是美国历史上生存最危险的年代？
print (crimes.idxmax(0))


