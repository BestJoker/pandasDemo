# coding:utf-8
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

'''
一.Series
Series是一种类似于一维数组的对象，它由一组数据（各种NumPy数据类型）以及一组与之相关的数据标签（即索引）组成
'''

obj = pd.Series([4,7,-5,3])
print (obj)
# 0    4
# 1    7
# 2   -5
# 3    3
# dtype: int64

print (obj.values)
#[ 4  7 -5  3]

print (obj.index)
#RangeIndex(start=0, stop=4, step=1)

obj2 = pd.Series([4,7,-5,3],index=['d','b','a','c'])
print (obj2)
# d    4
# b    7
# a   -5
# c    3
# dtype: int64

print (obj2.index)
#Index(['d', 'b', 'a', 'c'], dtype='object')

print (obj2['a'])
#-5

obj2['d'] = 6
print (obj2[['c','a','d']])
# c    3
# a   -5
# d    6
# dtype: int64


#使用NumPy函数或类似NumPy的运算（如根据布尔型数组进行过滤、标量乘法、应用数学函数等）都会保留索引值的链接：

print (obj2[obj2>0])
# d    6
# b    7
# c    3
# dtype: int64

print (obj2*2)
# d    12
# b    14
# a   -10
# c     6
# dtype: int64

print (np.exp(obj2))
# d     403.428793
# b    1096.633158
# a       0.006738
# c      20.085537
# dtype: float64

#它可以用在许多原本需要字典参数的函数中
print ('b' in obj2)#True
print ('e' in obj2)#False

#如果数据被存放在一个Python字典中，也可以直接通过这个字典来创建Series
sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
obj3 = pd.Series(sdata)
print (obj3)
# Ohio      35000
# Texas     71000
# Oregon    16000
# Utah       5000
# dtype: int64

states = ['California', 'Ohio', 'Oregon', 'Texas']
obj4 = pd.Series(sdata,index=states)
print (obj4)
# California        NaN
# Ohio          35000.0
# Oregon        16000.0
# Texas         71000.0
# dtype: float64
#sdata中跟states索引相匹配的那3个值会被找出来并放到相应的位置上，
#但由于"California"所对应的sdata值找不到，所以其结果就为NaN
#使用缺失（missing）或NA表示缺失数据。pandas的isnull和notnull函数可用于检测缺失数据

print (pd.isnull(obj4))
# California     True
# Ohio          False
# Oregon        False
# Texas         False
# dtype: bool

print (pd.notnull(obj4))
# California    False
# Ohio           True
# Oregon         True
# Texas          True
# dtype: bool

#Series最重要的一个功能是，它会根据运算的索引标签自动对齐数据,如果你使用过数据库，你可以认为是类似join的操作
print (obj3)
# Ohio      35000
# Texas     71000
# Oregon    16000
# Utah       5000
# dtype: int64
print (obj4)
# California        NaN
# Ohio          35000.0
# Oregon        16000.0
# Texas         71000.0
# dtype: float64
print (obj3+obj4)
# California         NaN
# Ohio           70000.0
# Oregon         32000.0
# Texas         142000.0
# Utah               NaN
# dtype: float64


#Series对象本身及其索引都有一个name属性，该属性跟pandas其他的关键功能关系非常密切：
obj4.name = 'population'
obj4.index.name = 'state'

print (obj4)
# state
# California        NaN
# Ohio          35000.0
# Oregon        16000.0
# Texas         71000.0
# Name: population, dtype: float64

print ('-------------------')

'''
二.DataFrame
DataFrame是一个表格型的数据结构，它含有一组有序的列，每列可以是不同的值类型（数值、字符串、布尔值等）。
DataFrame既有行索引也有列索引，它可以被看做由Series组成的字典（共用同一个索引）。
'''

#####DataFrame的创建
###①传入一个由等长列表或NumPy数组组成的字典
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002, 2003],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)
print (frame)
#     state  year  pop
# 0    Ohio  2000  1.5
# 1    Ohio  2001  1.7
# 2    Ohio  2002  3.6
# 3  Nevada  2001  2.4
# 4  Nevada  2002  2.9
# 5  Nevada  2003  3.2

print ('-------------------')

print (frame.head())#对于特别大的DataFrame，head方法会选取前五行

#如果指定了列序列，则DataFrame的列就会按照指定顺序进行排列：
pd.DataFrame(data,columns=['year','state','pop'])
#     state  year  pop
# 0    Ohio  2000  1.5
# 1    Ohio  2001  1.7
# 2    Ohio  2002  3.6
# 3  Nevada  2001  2.4
# 4  Nevada  2002  2.9

#如果传入的列在数据中找不到，就会在结果中产生缺失值：
frame2 = pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt'],index=['one', 'two', 'three', 'four','five', 'six'])
print (frame2)
#        year   state  pop debt
# one    2000    Ohio  1.5  NaN
# two    2001    Ohio  1.7  NaN
# three  2002    Ohio  3.6  NaN
# four   2001  Nevada  2.4  NaN
# five   2002  Nevada  2.9  NaN
# six    2003  Nevada  3.2  NaN

print (frame2['state'])#获取一列为一个Series
# one        Ohio
# two        Ohio
# three      Ohio
# four     Nevada
# five     Nevada
# six      Nevada
# Name: state, dtype: object

print (frame2.year)#点的方式也可以
# one      2000
# two      2001
# three    2002
# four     2001
# five     2002
# six      2003
# Name: year, dtype: int64

#笔记：IPython提供了类似属性的访问（即frame2.year）和tab补全。
#frame2[column]适用于任何列的名，但是frame2.column只有在列名是一个合理的Python变量名时才适用。

print (frame2.loc['three'])
# year     2002
# state    Ohio
# pop       3.6
# debt      NaN
# Name: three, dtype: object

#列可以通过赋值的方式进行修改
frame2['debt'] = 16.5
print (frame2)
#        year   state  pop  debt
# one    2000    Ohio  1.5  16.5
# two    2001    Ohio  1.7  16.5
# three  2002    Ohio  3.6  16.5
# four   2001  Nevada  2.4  16.5
# five   2002  Nevada  2.9  16.5
# six    2003  Nevada  3.2  16.5

frame2['debt'] = np.arange(6.)
print (frame2)

#将列表或数组赋值给某个列时，其长度必须跟DataFrame的长度相匹配。
#如果赋值的是一个Series，就会精确匹配DataFrame的索引，所有的空位都将被填上缺失值：
val = pd.Series([-1.2,-1.5,-1.7],index=['two','four','five'])
frame2['debt'] = val
print (frame2)
#        year   state  pop  debt
# one    2000    Ohio  1.5   NaN
# two    2001    Ohio  1.7  -1.2
# three  2002    Ohio  3.6   NaN
# four   2001  Nevada  2.4  -1.5
# five   2002  Nevada  2.9  -1.7
# six    2003  Nevada  3.2   NaN

#为不存在的列赋值会创建出一个新列。关键字del用于删除列。
#注意：不能用frame2.eastern创建新的列。

frame2['eastern'] = frame2.state == 'chio'
print (frame2)
#        year   state  pop  debt  eastern
# one    2000    Ohio  1.5   NaN    False
# two    2001    Ohio  1.7  -1.2    False
# three  2002    Ohio  3.6   NaN    False
# four   2001  Nevada  2.4  -1.5    False
# five   2002  Nevada  2.9  -1.7    False
# six    2003  Nevada  3.2   NaN    False

del frame2['eastern']#删除这列
print (frame2.columns)

# 注意：通过索引方式返回的列只是相应数据的视图而已，并不是副本。
# 因此，对返回的Series所做的任何就地修改全都会反映到源DataFrame上。
# 通过Series的copy方法即可指定复制列。

print ('-------------------')


###②嵌套字典
pop = {'Nevada': {2001: 2.4, 2002: 2.9},'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
frame3 = pd.DataFrame(pop)
print (frame3)
#       Nevada  Ohio
# 2001     2.4   1.7
# 2002     2.9   3.6
# 2000     NaN   1.5

#内层字典的键会被合并、排序以形成最终的索引。如果明确指定了索引，则不会这样：
print (pd.DataFrame(pop,index=[2001,2002,2003]))
#       Nevada  Ohio
# 2001     2.4   1.7
# 2002     2.9   3.6
# 2003     NaN   NaN

pdata = {'Ohio': frame3['Ohio'][:-1],'Nevada': frame3['Nevada'][:2]}
print (pd.DataFrame(pdata))
#       Ohio  Nevada
# 2001   1.7     2.4
# 2002   3.6     2.9

frame3.index.name = 'year'
frame3.columns.name = 'state'

print (frame3)
# state  Nevada  Ohio
# year
# 2001      2.4   1.7
# 2002      2.9   3.6
# 2000      NaN   1.5

print (frame3.values)
# [[2.4 1.7]
#  [2.9 3.6]
#  [nan 1.5]]

print ('-------------------')

'''
#####索引对象
'''
obj = pd.Series(range(3),index=['a','b','c'])
index = obj.index
print (index)
#Index(['a', 'b', 'c'], dtype='object')

print (index[1:])
#Index(['b', 'c'], dtype='object')

#Index对象是不可变的，因此用户不能对其进行修改：
#index[1] = 'd'  # TypeError

#与python的集合不同，pandas的Index可以包含重复的标签,选择重复的标签，会显示所有的结果
print ('-------------------')


'''
5.2 基本功能
①重新索引
'''
obj = pd.Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])
obj2 = obj.reindex(['a', 'b', 'c', 'd', 'e'])
print (obj2)
# a   -5.3
# b    7.2
# c    3.6
# d    4.5
# e    NaN
# dtype: float64

# 对于时间序列这样的有序数据，重新索引时可能需要做一些插值处理。
# method选项即可达到此目的，例如，使用ffill可以实现前向值填充：
obj3 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
print (obj3)
# 0      blue
# 2    purple
# 4    yellow
# dtype: object

obj3 = obj3.reindex(range(6), method='ffill')
print (obj3)
# 0      blue
# 1      blue
# 2    purple
# 3    purple
# 4    yellow
# 5    yellow
# dtype: object

print ('-------------------')

'''
#####丢弃指定轴上的项
丢弃某条轴上的一个或多个项很简单，只要有一个索引数组或列表即可。
由于需要执行一些数据整理和集合逻辑，所以drop方法返回的是一个在指定轴上删除了指定值的新对象：
'''
obj = pd.Series(np.arange(5.), index=['a', 'b', 'c', 'd', 'e'])
print (obj)
# a    0.0
# b    1.0
# c    2.0
# d    3.0
# e    4.0
# dtype: float64

new_obj = obj.drop('c')
print (new_obj)
# a    0.0
# b    1.0
# d    3.0
# e    4.0
# dtype: float64

print (obj.drop(['d','c']))
# a    0.0
# b    1.0
# e    4.0
# dtype: float64

#对于DataFrame，可以删除任意轴上的索引值


print ('-------------------')
data = pd.DataFrame(np.arange(16).reshape((4, 4)),index=['Ohio', 'Colorado', 'Utah', 'New York'],columns=['one', 'two', 'three', 'four'])
print (data)
#           one  two  three  four
# Ohio        0    1      2     3
# Colorado    4    5      6     7
# Utah        8    9     10    11
# New York   12   13     14    15

#用标签序列调用drop会从行标签（axis 0）删除值
print (data.drop(['Colorado','Ohio']))
#           one  two  three  four
# Utah        8    9     10    11
# New York   12   13     14    15

#通过传递axis=1或axis='columns'可以删除列的值：
print (data.drop('two',axis=1))
#           one  three  four
# Ohio        0      2     3
# Colorado    4      6     7
# Utah        8     10    11
# New York   12     14    15

#许多函数，如drop，会修改Series或DataFrame的大小或形状，可以就地修改对象，不会返回新的对象：
obj.drop('c',inplace=True)
print (obj)
# a    0.0
# b    1.0
# d    3.0
# e    4.0
# dtype: float64

print ('-------------------')

'''
#####索引、选取和过滤
'''
obj = pd.Series(np.arange(4.),index=['a','b','c','d'])
print (obj)
# a    0.0
# b    1.0
# c    2.0
# d    3.0
# dtype: float64

print (obj['b'])
#1.0

print (obj[1])
#1.0

print (obj[2:4])
# c    2.0
# d    3.0
# dtype: float64

print (obj[['b','a','d']])
# b    1.0
# a    0.0
# d    3.0
# dtype: float64

print (obj[[1,3]])
# b    1.0
# d    3.0
# dtype: float64

print (obj[obj<2])
# a    0.0
# b    1.0
# dtype: float64

#利用标签的切片运算与普通的Python切片运算不同，其末端是包含的
print (obj['b':'c'])
# b    1.0
# c    2.0
# dtype: float64

#用切片可以对Series的相应部分进行设置：
obj['b':'c'] = 5
print (obj)
# a    0.0
# b    5.0
# c    5.0
# d    3.0
# dtype: float64

#用一个值或序列对DataFrame进行索引其实就是获取一个或多个列：
data = pd.DataFrame(np.arange(16).reshape((4, 4)),index=['Ohio', 'Colorado', 'Utah', 'New York'],columns=['one', 'two', 'three', 'four'])
print (data)
#           one  two  three  four
# Ohio        0    1      2     3
# Colorado    4    5      6     7
# Utah        8    9     10    11
# New York   12   13     14    15

print (data['two'])
# Ohio         1
# Colorado     5
# Utah         9
# New York    13
# Name: two, dtype: int64
print (data[['three','two']])
#           three  two
# Ohio          2    1
# Colorado      6    5
# Utah         10    9
# New York     14   13

#这种索引方式有几个特殊的情况。首先通过切片或布尔型数组选取数据：
print (data[:2])
#           one  two  three  four
# Ohio        0    1      2     3
# Colorado    4    5      6     7

print (data[data['three'] > 5])
#           one  two  three  four
# Colorado    4    5      6     7
# Utah        8    9     10    11
# New York   12   13     14    15

'''
#####用loc和iloc进行选取
对于DataFrame的行的标签索引，我引入了特殊的标签运算符loc和iloc。
它们可以让你用类似NumPy的标记，使用轴标签（loc）或整数索引（iloc），从DataFrame选择行和列的子集。
'''
#①让我们通过标签选择一行和多列：
print (data.loc['Colorado', ['two', 'three']])
# two      5
# three    6
# Name: Colorado, dtype: int64

#②用iloc和整数进行选取
print (data.iloc[2,[3,0,1]])
# four    11
# one      8
# two      9
# Name: Utah, dtype: int64

print (data.iloc[2])
# one       8
# two       9
# three    10
# four     11
# Name: Utah, dtype: int64

print (data.iloc[[1,2],[3,0,1]])
#           four  one  two
# Colorado     7    4    5
# Utah        11    8    9

#这两个索引函数也适用于一个标签或多个标签的切片：
print (data.loc[:'Utah','two'])

print (data.iloc[:,:3][data.three > 5])
#           one  two  three
# Colorado    4    5      6
# Utah        8    9     10
# New York   12   13     14


print ('-------------------')

'''
#####整数索引
如果轴索引含有整数，数据选取总会使用标签。为了更准确，请使用loc（标签）或iloc（整数）
'''
ser = pd.Series(np.arange(3.))
print (ser)
# 0    0.0
# 1    1.0
# 2    2.0
# dtype: float64

print (ser[:1])
# 0    0.0
# dtype: float64

print (ser.loc[:1])
# 0    0.0
# 1    1.0
# dtype: float64

print (ser.iloc[:1])
# 0    0.0
# dtype: float64

print ('-------------------')

'''
算术运算和数据对齐
pandas最重要的一个功能是，它可以对不同索引的对象进行算术运算。
在将对象相加时，如果存在不同的索引对，则结果的索引就是该索引对的并集。
'''

s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1],index=['a', 'c', 'e', 'f', 'g'])
print (s1)
# a    7.3
# c   -2.5
# d    3.4
# e    1.5
# dtype: float64

print (s2)
# a   -2.1
# c    3.6
# e   -1.5
# f    4.0
# g    3.1
# dtype: float64

print (s1 + s2)
# a    5.2
# c    1.1
# d    NaN
# e    0.0
# f    NaN
# g    NaN
# dtype: float64

#自动的数据对齐操作在不重叠的索引处引入了NA值。缺失值会在算术运算过程中传播。

df1 = pd.DataFrame(np.arange(9.).reshape((3, 3)), columns=list('bcd'),index=['Ohio', 'Texas', 'Colorado'])

df2 = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns=list('bde'),index=['Utah', 'Ohio', 'Texas', 'Oregon'])

print (df1)
#             b    c    d
# Ohio      0.0  1.0  2.0
# Texas     3.0  4.0  5.0
# Colorado  6.0  7.0  8.0

print (df2)
#           b     d     e
# Utah    0.0   1.0   2.0
# Ohio    3.0   4.0   5.0
# Texas   6.0   7.0   8.0
# Oregon  9.0  10.0  11.0

print (df1+df2)
#             b   c     d   e
# Colorado  NaN NaN   NaN NaN
# Ohio      3.0 NaN   6.0 NaN
# Oregon    NaN NaN   NaN NaN
# Texas     9.0 NaN  12.0 NaN
# Utah      NaN NaN   NaN NaN

print ('-------------------')

'''
DataFrame和Series之间的运算
'''
arr = np.arange(12.).reshape((3,4))
print (arr)
# [[ 0.  1.  2.  3.]
#  [ 4.  5.  6.  7.]
#  [ 8.  9. 10. 11.]]

print (arr[0])
#[0. 1. 2. 3.]

print (arr - arr[0])
# [[0. 0. 0. 0.]
#  [4. 4. 4. 4.]
#  [8. 8. 8. 8.]]

#当我们从arr减去arr[0]，每一行都会执行这个操作。这就叫做广播（broadcasting）

frame = pd.DataFrame(np.arange(12.).reshape((4, 3)),columns=list('bde'),index=['Utah', 'Ohio', 'Texas', 'Oregon'])

series = frame.iloc[0]

print (frame)
#           b     d     e
# Utah    0.0   1.0   2.0
# Ohio    3.0   4.0   5.0
# Texas   6.0   7.0   8.0
# Oregon  9.0  10.0  11.0

print (series)
# b    0.0
# d    1.0
# e    2.0
# Name: Utah, dtype: float64

print (frame - series)
#           b    d    e
# Utah    0.0  0.0  0.0
# Ohio    3.0  3.0  3.0
# Texas   6.0  6.0  6.0
# Oregon  9.0  9.0  9.0

print ('-------------------')

'''
函数应用和映射
①NumPy的ufuncs（元素级数组方法）也可用于操作pandas对象
②将函数应用到由各列或行所形成的一维数组上
'''
frame = pd.DataFrame(np.random.randn(4,3),columns=list('bde'),index=['Utah','Ohio','Texas','Oregon'])

print (frame)
#                b         d         e
# Utah   -0.106394  0.642617 -0.235295
# Ohio    0.473762  1.487093 -1.182141
# Texas   1.341141  0.364937  0.226267
# Oregon  0.423306 -0.180981 -0.494756

print (np.abs(frame))
#                b         d         e
# Utah    0.106394  0.642617  0.235295
# Ohio    0.473762  1.487093  1.182141
# Texas   1.341141  0.364937  0.226267
# Oregon  0.423306  0.180981  0.494756

f = lambda x: x.max() - x.min()
print (frame.apply(f))
# b    1.605575
# d    2.677043
# e    0.610599
# dtype: float64

# 这里的函数f，计算了一个Series的最大值和最小值的差，
# 在frame的每列都执行了一次。结果是一个Series，使用frame的列作为索引。
print ('-------------------')

'''
排序和排名
要对行或列索引进行排序（按字典顺序），可使用sort_index方法，它将返回一个已排序的新对象：
'''
obj = pd.Series(range(4),index=['d','a','b','c'])
print (obj.sort_index())
# a    1
# b    2
# c    3
# d    0
# dtype: int64

frame = pd.DataFrame(np.arange(8).reshape((2,4)),index=['three','one'],columns=['d','a','b','c'])
print (frame)
#        d  a  b  c
# three  0  1  2  3
# one    4  5  6  7

print (frame.sort_index())
#        d  a  b  c
# one    4  5  6  7
# three  0  1  2  3

print (frame.sort_index(axis=1,ascending=False))
#        d  c  b  a
# three  0  3  2  1
# one    4  7  6  5

#若要按值对Series进行排序，可使用其sort_values方法：
obj = pd.Series([4, 7, -3, 2])
print (obj.sort_values())
# 2   -3
# 3    2
# 0    4
# 1    7
# dtype: int64

#在排序时，任何缺失值默认都会被放到Series的末尾：
obj = pd.Series([4, np.nan, 7, np.nan, -3, 2])
print (obj.sort_values())
# 4   -3.0
# 5    2.0
# 0    4.0
# 2    7.0
# 1    NaN
# 3    NaN
# dtype: float64

# 当排序一个DataFrame时，你可能希望根据一个或多个列中的值进行排序。
# 将一个或多个列的名字传递给sort_values的by选项即可达到该目的：
frame = pd.DataFrame({'b': [4, 7, -3, 2], 'a': [0, 1, 0, 1]})
print (frame)
#    b  a
# 0  4  0
# 1  7  1
# 2 -3  0
# 3  2  1

print (frame.sort_values(by='b'))
#    b  a
# 2 -3  0
# 3  2  1
# 0  4  0
# 1  7  1

print (frame.sort_values(by=['b','a']))
#    b  a
# 2 -3  0
# 3  2  1
# 0  4  0
# 1  7  1

print ('-------------------')

'''
5.3 汇总和计算描述统计
'''
df = pd.DataFrame([[1.4, np.nan], [7.1, -4.5],[np.nan, np.nan], [0.75, -1.3]], index=['a', 'b', 'c', 'd'],columns=['one', 'two'])
print (df)
#     one  two
# a  1.40  NaN
# b  7.10 -4.5
# c   NaN  NaN
# d  0.75 -1.3

print (df.sum())
# one    9.25
# two   -5.80
# dtype: float64

#传入axis='columns'或axis=1将会按行进行求和运算：
print (df.sum(axis=1))
# a    1.40
# b    2.60
# c    0.00
# d   -0.55
# dtype: float64

#有些方法（如idxmin和idxmax）返回的是间接统计（比如达到最小值或最大值的索引）：
print (df.idxmax())


print ('-------------------')
