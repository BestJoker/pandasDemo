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

#8.两个series的交集
print ('-'*20+'8')
ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])
print (np.intersect1d(ser1,ser2))

#9.两个series的非共有元素
print ('-'*20+'9')
u = pd.Series(np.union1d(ser1,ser2))
i = pd.Series(np.intersect1d(ser1,ser2))
res = u[~u.isin(i)]
print (res)

#10.如何获得series的最小值，第25百分位数，中位数，第75位和最大值？
print ('-'*20+'10')
ser = pd.Series(np.random.normal(10,5,25))
np.random.RandomState(100)
print (np.percentile(ser,q=[0,25,50,75,100]))

#11.如何获得系列中唯一项目的频率计数？
print ('-'*20+'11')
ser = pd.Series(np.take(list('abcdefgh'),np.random.randint(8,size=30)))
print (ser)
print (ser.value_counts())

#12.series中计数排名前2的元素
print ('-'*20+'12')
v_cnt = ser.value_counts()
print (v_cnt)
print (v_cnt.value_counts())
cnt_cnt = v_cnt.value_counts().index[:2]
print (cnt_cnt)

#13.如何将数字系列分成10个相同大小的组
print ('-'*20+'13')

#14.如何将numpy数组转换为给定形状的dataframe
print ('-'*20+'14')
ser = pd.Series(np.random.randint(1, 10, 35))
df = pd.DataFrame(ser.values.reshape(7,5))
print (df)

#15.如何从一系列中找到2的pd倍数的数字位置:argwhere
print ('-'*20+'15')
ser = pd.Series(np.random.randint(1,10,7))
print (ser)
print (np.argwhere(ser % 2 == 0))

#16.如何从系列中的给定位置提取项目:take
print ('-'*20+'16')
ser = pd.Series(list('abcdefghijklmnopqrstuvwxyz'))
pos = [0,4,8,14,20]
ser.take(pos)

#17.获取元素的位置:get_loc
aims = list('adhz')
for i in aims:
    print (i)
    n = pd.Index(ser).get_loc(i)
    print (n)

#18.如何将系列中每个元素的第一个字符转换为大写
ser = pd.Series(['how', 'to', 'kick', 'ass?'])
ser = ser.map(lambda x:x.title())
print (ser)

#19.如何计算系列中每个单词的字符数
print ('-'*20+'19')
print (ser.map(lambda x:len(x)))

#20.series如何将一日期字符串转换为时间
print ('-'*20+'20')
ser = pd.Series(['01 Jan 2010',
                '02-02-2011',
                 '20120303',
                 '2013/04/04',
                 '2014-05-05',
                 '2015-06-06T12:20'])
print (pd.to_datetime(ser))

#21.series如何从时间序列中提取年/月/天/小时/分钟/秒
print ('-'*20+'21')

date = pd.Series(['01 Jan 2010',
                '02-02-2011',
                 '20120303',
                 '2013/04/04',
                 '2014-05-05',
                 '2015-06-06T12:20'])
date = pd.to_datetime(date)
print (date.dt.year)
print (date.dt.month)
print (date.dt.day)
print (date.dt.hour)



#22.从series中找出包含两个以上元音字母的单词
print ('-'*20+'22')
ser = pd.Series(['Apple', 'Orange', 'Plan', 'Python', 'Money'])
def count(x):
    aims = 'aeiou'
    c = 0
    for i in x:
        if i in aims:
            c+=1
    return c

counts = ser.map(lambda x:count(x))
print (ser[counts>=2])

#23.series A 以series B为分组依据, 然后计算分组后的平均值
print ('-'*20+'23')
fruit = pd.Series(np.random.choice(['apple', 'banana', 'carrot'], 10))
weights = pd.Series(np.linspace(1, 10, 10))
weights.groupby(fruit).mean()

#24.如何创建一个以’2000-01-02’开始包含10个周六的TimeSeries
print ('-'*20+'24')
pd.Series(np.random.randint(1,10,10),pd.date_range('2000-01-02',periods=10,freq='W-SAT'))

#25.从dataframe中找到a列最大值对应的行
print ('-'*20+'25')
df=pd.DataFrame(
    {
        'a':range(100),
        'b':np.random.rand(100),
        'c':[1,2,3,4]*25,
        'd':['apple', 'banana', 'carrot']*33 + ['apple']
    }
)
print (df)
print (df.loc[df.a == np.max(df.a)])

#26.从dataframe中获取c列最大值所在的行号
print ('-'*20+'26')
print (np.where(df.c==np.max(df.c)))

#27.在dataframe中根据行列数读取某个值
print ('-'*20+'27')
row = 4
col = 0
print ('行{row}列{col}的值是：{df.iat[row,col]}')

#28.在dataframe中根据index和列名称读取某个值
print ('-'*20+'28')
row = 4
col = 0
print('行{row}列{col}的值是: {df.iat[row, col]}')

#29.dataframe中重命名某一列
print ('-'*20+'29')
print (df.rename(columns={'d':'fruit'}).head())

#30.检查dataframe是否有缺失值
print ('-'*20+'30')
df = pd.DataFrame({
    'a':[1.2,2,3,4],
    'b':list('abcd')
})
print ('缺失：',df.isnull().values.any())
print (df.isnull())
df.iat[0,0] = np.nan
print ('缺失：',df.isnull().values.any())

#31.统计dataframe中每列缺失值的数量
print ('-'*20+'31')
df.apply(lambda x:x.isnull().sum())

#32.dataframe用每列的平均值取代缺失值
print ('-'*20+'32')
df = pd.DataFrame({
    'a':[1.2,2,3,4],
    'b':[2,np.nan,4,np.nan],
    'c':[12,13,45,35]
})
print (df.apply(lambda x:x.fillna(x.mean())))

#33.从dataframe中获取某一列, 并返回一个dataframe
print ('-'*20+'33')
print (df[['a','b']])

#34.dataframe如何改变列的顺序
print ('-'*20+'34')
df = pd.DataFrame(np.arange(20).reshape(-1, 5), columns=list('abcde'))
print (df)
df = df[list('cbdae')]
print (df)

#35.设置dataframe输出的行数和列数
print ('-'*20+'35')
# pd.set_option('display.max_columns',3)
# pd.set_option('display.max_rows',3)
print (df)

#36.设置dataframe输出百分比数据
print ('-'*20+'36')
df=pd.DataFrame(
    {
        'a':range(100),
        'b':np.random.rand(100),
        'c':[1,2,3,4]*25,
        'd':['apple', 'banana', 'carrot']*33 + ['apple']
    }
)
print (df)
df.style.format({'b':'{0:.2%}'.format})
print (df)



#37.获取第n大的数所在行
print ('-'*20+'37')
df = pd.DataFrame(
    np.random.randint(1, 30, 30).reshape(10,-1),
    columns=list('abc'))
print (df)
print (df['a'])
# 使用行号排序
df['a'].argsort()

#38.dataframe获取行之和大于100的数据, 并返回最后的两行
print ('-'*20+'38')
df = pd.DataFrame(np.random.randint(10, 40, 60).reshape(-1, 4))
print (df)

#39.计算每一行的最小值与最大值的比值
print ('-'*20+'39')

df = pd.DataFrame(np.random.randint(1,100, 80).reshape(8, -1))
print (df)
min_by_max = df.apply(lambda x:np.min(x)/np.max(x) ,axis=1)
df['min_by_max'] = min_by_max
print (df)

#40.找到每行第二大的值
print ('-'*20+'40')
df = pd.DataFrame(np.random.randint(1,100, 80).reshape(8, -1))
print (df)
out = df.apply(lambda x:x.sort_values().unique()[-2],axis=1)
df['out'] = out
print (df)

#41.dataframe分组后获取某个组的数据
print ('-'*20+'41')
df = pd.DataFrame({'col1': ['apple', 'banana', 'orange'] * 3,
                   'col2': np.random.rand(9),
                   'col3': np.random.randint(0, 15, 9)})
print (df)
grouped = df.groupby(by=['col1'])
print (grouped.get_group('apple'))

#42.分组后获取某组中的第n大的值
print ('-'*20+'42')
df = pd.DataFrame({'fruit': ['apple', 'banana', 'orange'] * 3,
                   'taste': np.random.rand(9),
                   'price': np.random.randint(0, 15, 9)})
n = 2
grouped = df['taste'].groupby(df.fruit)
print (grouped.get_group('banana').sort_values().iloc[-n])
print (type(grouped.get_group('banana')))

print (df.groupby(by=['fruit']).get_group('banana')['taste'].sort_values().iloc[-n])
print (type(df.groupby(by=['fruit']).get_group('banana')['taste']))


# print ('-'*20+'6')


