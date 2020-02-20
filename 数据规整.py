# coding:utf-8
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

'''
#####8.1 层次化索引
层次化索引（hierarchical indexing）是pandas的一项重要功能，它使你能在一个轴上拥有多个（两个以上）索引级别。
抽象点说，它使你能以低维度形式处理高维度数据。
'''
data = Series(np.random.randn(9),index=[['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd'], [1, 2, 3, 1, 3, 1, 2, 2, 3]])

print (data)

# a  1   -0.832174
#    2   -0.588509
#    3    1.238672
# b  1    0.002234
#    3    1.368472
# c  1    1.307679
#    2   -0.933680
# d  2   -0.348803
#    3    0.387536
# dtype: float64

print (data.index)
# MultiIndex([('a', 1),
#             ('a', 2),
#             ('a', 3),
#             ('b', 1),
#             ('b', 3),
#             ('c', 1),
#             ('c', 2),
#             ('d', 2),
#             ('d', 3)],
#            )

print (data['b'])
# 1    0.002234
# 3    1.368472
# dtype: float64

print (data['b':'c'])
# b  1    0.002234
#    3    1.368472
# c  1    1.307679
#    2   -0.933680
# dtype: float64

print (data.loc[['b','d']])
# b  1    0.002234
#    3    1.368472
# d  2   -0.348803
#    3    0.387536
# dtype: float64

print (data.loc[:,2])
# a   -0.588509
# c   -0.933680
# d   -0.348803
# dtype: float64

print ('-------------------')

frame = pd.DataFrame(np.arange(12).reshape((4, 3)),index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]],columns=[['Ohio', 'Ohio', 'Colorado'],['Green', 'Red', 'Green']])

print (frame)
#      Ohio     Colorado
#     Green Red    Green
# a 1     0   1        2
#   2     3   4        5
# b 1     6   7        8
#   2     9  10       11

#各层都可以有名字（可以是字符串，也可以是别的Python对象）。如果指定了名称，它们就会显示在控制台输出中：
frame.index.names = ['key1','key2']
frame.columns.names = ['state','color']
print (frame)

# state      Ohio     Colorado
# color     Green Red    Green
# key1 key2
# a    1        0   1        2
#      2        3   4        5
# b    1        6   7        8
#      2        9  10       11

print (frame['Ohio'])
# color      Green  Red
# key1 key2
# a    1         0    1
#      2         3    4
# b    1         6    7
#      2         9   10

print ('-------------------')

'''
###重排与分级排序
有时，你需要重新调整某条轴上各级别的顺序，或根据指定级别上的值对数据进行排序。
swaplevel:接受两个级别编号或名称，并返回一个互换了级别的新对象（但数据不会发生变化）
sort_index:根据单个级别中的值对数据进行排序
'''

print (frame.swaplevel('key1','key2'))
# state      Ohio     Colorado
# color     Green Red    Green
# key2 key1
# 1    a        0   1        2
# 2    a        3   4        5
# 1    b        6   7        8
# 2    b        9  10       11

print (frame.sort_index(level=1))
# state      Ohio     Colorado
# color     Green Red    Green
# key1 key2
# a    1        0   1        2
# b    1        6   7        8
# a    2        3   4        5
# b    2        9  10       11

print (frame.swaplevel(0, 1).sort_index(level=0))
# state      Ohio     Colorado
# color     Green Red    Green
# key2 key1
# 1    a        0   1        2
#      b        6   7        8
# 2    a        3   4        5
#      b        9  10       11

'''
###根据级别汇总统计
level选项，它用于指定在某条轴上求和的级别
'''
print (frame.sum(level='key2'))
# state  Ohio     Colorado
# color Green Red    Green
# key2
# 1         6   8       10
# 2        12  14       16

print (frame.sum(level='color',axis=1))
# color      Green  Red
# key1 key2
# a    1         2    1
#      2         8    4
# b    1        14    7
#      2        20   10

print ('-------------------')


'''
###使用DataFrame的列进行索引
set_index:将其一个或多个列转换为行索引，并创建一个新的DataFrame,默认情况下，
那些列会从DataFrame中移除,drop=False可以把他们留下来
reset_index：跟set_index刚好相反，层次化索引的级别会被转移到列里面
'''

frame = pd.DataFrame({'a': range(7), 'b': range(7, 0, -1),
                      'c': ['one', 'one', 'one', 'two', 'two','two', 'two'],
                      'd': [0, 1, 2, 0, 1, 2, 3]})

print (frame)
#    a  b    c  d
# 0  0  7  one  0
# 1  1  6  one  1
# 2  2  5  one  2
# 3  3  4  two  0
# 4  4  3  two  1
# 5  5  2  two  2
# 6  6  1  two  3

frame2 = frame.set_index(['c','d'])
print (frame2)
#        a  b
# c   d
# one 0  0  7
#     1  1  6
#     2  2  5
# two 0  3  4
#     1  4  3
#     2  5  2
#     3  6  1

print (frame2.reset_index())
#      c  d  a  b
# 0  one  0  0  7
# 1  one  1  1  6
# 2  one  2  2  5
# 3  two  0  3  4
# 4  two  1  4  3
# 5  two  2  5  2
# 6  two  3  6  1

print ('-------------------')

'''
#####8.2 合并数据集
pandas.merge可根据一个或多个键将不同DataFrame中的行连接起来。SQL或其他关系型数据库的用户对此应该会比较熟悉，
因为它实现的就是数据库的join操作。
pandas.concat可以沿着一条轴将多个对象堆叠到一起。
实例方法combine_first可以将重复数据拼接在一起，用一个对象中的值填充另一个对象中的缺失值。
'''

'''
###数据库风格的DataFrame合并
数据集的合并（merge）或连接（join）运算是通过一个或多个键将行连接起来的。
①如果有相同的列标签则自动可以关联
②如果没有相同的列标签，需要使用left_on和right_on字段明确链接字段

默认情况下，merge做的是“内连接”；结果中的键是交集。
其他方式还有"left"、"right"以及"outer"。外连接求取的是键的并集，组合了左连接和右连接的效果
'''

df1 = pd.DataFrame({'key':['b','b','a','c','a','a','b'],
                    'data1':range(7)})
df2 = pd.DataFrame({'key':['a','b','d'],
                    'data2':range(3)})

print (df1)
#   key  data1
# 0   b      0
# 1   b      1
# 2   a      2
# 3   c      3
# 4   a      4
# 5   a      5
# 6   b      6

print (df2)
#   key  data2
# 0   a      0
# 1   b      1
# 2   d      2

#如果没有指定，merge就会将重叠列的列名当做键
print (pd.merge(df1,df2))
#   key  data1  data2
# 0   b      0      1
# 1   b      1      1
# 2   b      6      1
# 3   a      2      0
# 4   a      4      0
# 5   a      5      0

#最好明确指定一下，某个列作为键
print (pd.merge(df1,df2,on='key'))
#   key  data1  data2
# 0   b      0      1
# 1   b      1      1
# 2   b      6      1
# 3   a      2      0
# 4   a      4      0
# 5   a      5      0

print ('-------------------')

df3 = pd.DataFrame({'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],'data1': range(7)})
df4 = pd.DataFrame({'rkey': ['a', 'b', 'd'],'data2': range(3)})

print (df3)
#   lkey  data1
# 0    b      0
# 1    b      1
# 2    a      2
# 3    c      3
# 4    a      4
# 5    a      5
# 6    b      6

print (df4)
#   rkey  data2
# 0    a      0
# 1    b      1
# 2    d      2

print ('-------------------')

print (pd.merge(df3,df4,left_on='lkey',right_on='rkey'))
#   lkey  data1 rkey  data2
# 0    b      0    b      1
# 1    b      1    b      1
# 2    b      6    b      1
# 3    a      2    a      0
# 4    a      4    a      0
# 5    a      5    a      0

#merge做的是“内连接”，结果中的键是交集。外连接求取的是键的并集，组合了左连接和右连接的效果
print (pd.merge(df1,df2,how='outer'))
#   key  data1  data2
# 0   b    0.0    1.0
# 1   b    1.0    1.0
# 2   b    6.0    1.0
# 3   a    2.0    0.0
# 4   a    4.0    0.0
# 5   a    5.0    0.0
# 6   c    3.0    NaN
# 7   d    NaN    2.0

print (pd.merge(df1,df2,how='left'))
#   key  data1  data2
# 0   b      0    1.0
# 1   b      1    1.0
# 2   a      2    0.0
# 3   c      3    NaN
# 4   a      4    0.0
# 5   a      5    0.0
# 6   b      6    1.0

print (pd.merge(df1,df2,how='right'))
#   key  data1  data2
# 0   b    0.0      1
# 1   b    1.0      1
# 2   b    6.0      1
# 3   a    2.0      0
# 4   a    4.0      0
# 5   a    5.0      0
# 6   d    NaN      2


'''
###轴向连接
另一种数据合并运算也被称作连接（concatenation）、绑定（binding）或堆叠（stacking）
'''
