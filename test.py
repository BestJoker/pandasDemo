# coding:utf-8
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

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
#print (crime.head(15))
#print (crime.info())

# -- 将Year的数据类型转换为 datetime64
crime.Year = pd.to_datetime(crime['Year'],format='%Y')
#print (df)

# -- 将列Year设置为数据框的索引
crime = crime.set_index('Year',drop=True)
#print (crime)

# -- 删除名为Total的列
del crime['Total']
#print (crime.info())

# -- 按照Year（每十年）对数据框进行分组并求和
crimes = crime.resample('10AS').sum()
population = crime.resample('10AS').max()
crimes['Population'] = population
#print (crimes)

# -- 何时是美国历史上生存最危险的年代？
#print (crimes.idxmax(0))


'''
#####练习5-合并¶

探索虚拟姓名数据
-- 创建DataFrame
-- 将上述的DataFrame分别命名为data1, data2, data3
-- 将data1和data2两个数据框按照行的维度进行合并，命名为all_data
-- 将data1和data2两个数据框按照列的维度进行合并，命名为all_data_col
-- 打印data3
-- 按照subject_id的值对all_data和data3作合并
-- 对data1和data2按照subject_id作内连接
-- 找到 data1 和 data2 合并之后的所有匹配结果
'''

# -- 创建DataFrame
raw_data_1 = {
        'subject_id': ['1', '2', '3', '4', '5'],
        'first_name': ['Alex', 'Amy', 'Allen', 'Alice', 'Ayoung'],
        'last_name': ['Anderson', 'Ackerman', 'Ali', 'Aoni', 'Atiches']}

raw_data_2 = {
        'subject_id': ['4', '5', '6', '7', '8'],
        'first_name': ['Billy', 'Brian', 'Bran', 'Bryce', 'Betty'],
        'last_name': ['Bonder', 'Black', 'Balwner', 'Brice', 'Btisan']}

raw_data_3 = {
        'subject_id': ['1', '2', '3', '4', '5', '7', '8', '9', '10', '11'],
        'test_id': [51, 15, 15, 61, 16, 14, 15, 1, 61, 16]}

# -- 将上述的DataFrame分别命名为data1, data2, data3

data1 = pd.DataFrame(raw_data_1)
data2 = pd.DataFrame(raw_data_2)
data3 = pd.DataFrame(raw_data_3)

# -- 将data1和data2两个数据框按照行的维度进行合并，命名为all_data
all_data = pd.concat([data1,data2],axis=0)
# print (all_data)

# -- 将data1和data2两个数据框按照列的维度进行合并，命名为all_data_col
all_data_col = pd.concat([data1,data2],axis=1)
# print (all_data_col)

# -- 打印data3
# print (data3)

# -- 按照subject_id的值对all_data和data3作合并
df = pd.merge(all_data,data3,on='subject_id')
# print (df)

# -- 对data1和data2按照subject_id作内连接
df = pd.merge(data1,data2,on='subject_id',how='inner')
#print (df)

# -- 找到 data1 和 data2 合并之后的所有匹配结果
pd.merge(data1,data2,on='subject_id',how='outer')


'''
#####练习6-统计
探索风速数据
-- 将数据作存储并且设置前三列为合适的索引
-- 2061年？我们真的有这一年的数据？创建一个函数并用它去修复这个bug
-- 将日期设为索引，注意数据类型，应该是datetime64[ns]
-- 对应每一个location，一共有多少数据值缺失
-- 对应每一个location，一共有多少完整的数据值
-- 对于全体数据，计算风速的平均值
-- 创建一个名为loc_stats的数据框去计算并存储每个location的风速最小值，最大值，平均值和标准差
-- 创建一个名为day_stats的数据框去计算并存储所有location的风速最小值，最大值，平均值和标准差
-- 对于每一个location，计算一月份的平均风速
-- 对于数据记录按照年为频率取样
-- 对于数据记录按照月为频率取样
'''

# -- 将数据作存储并且设置前三列为合适的索引
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(PROJECT_ROOT,'Pandas_exercises-master/wind.csv')
wind = pd.read_csv(path)
#print (wind.head(20))
#print (wind.columns)

# -- 2061年？我们真的有这一年的数据？创建一个函数并用它去修复这个bug
# -- 将日期设为索引，注意数据类型，应该是datetime64[ns]
# -- 对应每一个location，一共有多少数据值缺失
# -- 对应每一个location，一共有多少完整的数据值
# -- 对于全体数据，计算风速的平均值
# -- 创建一个名为loc_stats的数据框去计算并存储每个location的风速最小值，最大值，平均值和标准差
# -- 创建一个名为day_stats的数据框去计算并存储所有location的风速最小值，最大值，平均值和标准差
# -- 对于每一个location，计算一月份的平均风速
# -- 对于数据记录按照年为频率取样
# -- 对于数据记录按照月为频率取样



'''
#####练习7-可视化
探索泰坦尼克灾难数据
-- 将数据框命名为titanic
-- 将PassengerId设置为索引
-- 绘制一个展示男女乘客比例的扇形图
-- 绘制一个展示船票Fare, 与乘客年龄和性别的散点图
-- 有多少人生还？
-- 绘制一个展示船票价格的直方图
'''

# -- 将数据框命名为titanic
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(PROJECT_ROOT,'Pandas_exercises-master/train.csv')
titanic = pd.read_csv(path)
print (titanic.head(10))
print (titanic.columns)

# -- 将PassengerId设置为索引
titanic = titanic.set_index('PassengerId')
print (titanic.head(10))

# -- 绘制一个展示男女乘客比例的扇形图
Male = (titanic.Sex == 'male').sum()
Female = (titanic.Sex == 'female').sum()
proportions = [Male,Female]
plt.pie(proportions,labels=['Male','Female'],shadow=True,autopct='%1.1f%%',startangle=90,explode=(0.15,0))
plt.axis('equal')
plt.title('Sex Propertion')
plt.tight_layout()
plt.show()

# -- 绘制一个展示船票Fare, 与乘客年龄和性别的散点图
# lm = sns.lmplot(x='Age',y='Fare',data=titanic,hue='Sex',fit_reg=False)
# lm.set(title='Fare x Age')
# #设置坐标轴取值范围
# axes = lm.axes
# axes[0,0].set_ylim(-5,)
# axes[0,0].set_xlim(-5,85)

# -- 有多少人生还？
titanic.Survived.sum()


# -- 绘制一个展示船票价格的直方图
df = titanic.Fare.sort_values(ascending=False)
plt.hist(df,bins=(np.arange(0,600,100)))
plt.xlabel('Fare')
plt.ylabel('Frequency')
plt.title('Fare Payed Histrogram')
plt.show()

