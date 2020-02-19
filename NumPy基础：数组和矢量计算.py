# coding:utf-8
import pandas as pd
import numpy as np

#4.1 NumPy的ndarray：一种多维数组对象
data = np.random.randn(2,3)
print (data)

#数学运算

#所有的元素都乘以10
print (data * 10)
#每个元素都与自身相加
print (data + data)

'''
4.1 NumPy的ndarray：一种多维数组对象
ndarray是一个通用的同构数据多维容器，也就是说，其中的所有元素必须是相同类型的。
每个数组都有一个shape（一个表示各维度大小的元组）和一个dtype（一个用于说明数组数据类型的对象）
'''
print (data.shape)
print (data.dtype)
print ('-----------')

'''
创建ndarray
①使用array函数
'''
data1 = [6,7.5,8,0,1]
arr1 = np.array(data1)
print (arr1)
print ('-----------')

data2 = [[1,2,3,4],[5,6,7,8]]
arr2 = np.array(data2)
print (arr2)
print (arr2.ndim)#ndim表示数组的维度，层级数
print (arr2.shape)
print ('-----------')

#dtype表示数组中数据类型
print (arr1.dtype)
print (arr2.dtype)
print ('-----------')

'''
②ones，zeros，full，eye
#np.ones(shape)：根据shape生成一个全1数组，shape是元组类型，比如(2,3)；
#np.zeros(shape)：根据shape生成一个全0数组，shape是元组类型，比如(2,3,4)；
#np.full(shape,val)：根据shape生成一个数组，每个元素值都是val；
#np.eye(n)：创建一个正方的n*n单位矩阵，对角线为1，其余为0；
'''

print (np.ones((2,3)))
# [[1. 1. 1.]
#  [1. 1. 1.]]
 
print (np.zeros(10))
# [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]

print (np.zeros((3,6)))
# [[0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0.]]
 
print (np.full((3,5),6))
# [[6 6 6 6 6]
#  [6 6 6 6 6]
#  [6 6 6 6 6]]
 
print (np.eye(3,3))
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]
 
print ('-----------')

'''
③arange
#np.arange(begin,end,step,dtype=np.float32)begin为元素起始值（包含），
end为元素结束值（不包含），step为步长（默认值为1），dtype为元素类型。
如果只有一个参数n，则为从0到n-1；如有有两个参数n和m，则为从n到m-1；
'''
print (np.arange(10,20,2))
#[10 12 14 16 18]

print (np.arange(12).reshape(3,4))
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
print ('-----------')


#ndarray的数据类型
arr1 = np.array([1,2,3],dtype=np.float64)
arr2 = np.array([1,2,3],dtype=np.int32)
print (arr1.dtype)#float64
print (arr2.dtype)#int32
print ('-----------')

#将一个数组从一个dtype转换成另一个dtype
arr3 = arr1.astype(np.int32)
print (arr3.dtype)#int32
print (arr1)
# [1. 2. 3.]
print (arr3)
# [1 2 3]
print ('-----------')

#如果某字符串数组表示的全是数字，也可以用astype将其转换为数值形式：
numeric_strings = np.array(['1.23','-9.6','24'],dtype=np.string_)
print (numeric_strings.astype(float))
#[ 1.23 -9.6  24.  ]
print ('-----------')


'''
NumPy数组的运算
'''
arr = np.array([[1,2,3],[4,5,6]])

#①大小相等的数组之间的任何算术运算都会将运算应用到元素级：
print (arr)
# [[1 2 3]
#  [4 5 6]]
print (arr * arr)
# [[ 1  4  9]
#  [16 25 36]]
print (arr - arr)
# [[0 0 0]
#  [0 0 0]]

#②数组与标量的算术运算会将标量值传播到各个元素：
print (1/arr)
# [[1.         0.5        0.33333333]
#  [0.25       0.2        0.16666667]]
print (arr * 0.05)
# [[0.05 0.1  0.15]
#  [0.2  0.25 0.3 ]]
#③大小相同的数组之间的比较会生成布尔值数组：
arr2 = np.array([[0,3,2],[6,3,8]])
print (arr > arr2)
# [[ True False  True]
#  [False  True False]]

print ('-----------')

'''
基本的索引和切片
'''
#一维数组

arr = np.arange(10)
print (arr)
#[0 1 2 3 4 5 6 7 8 9]

print (arr[5])
#5

print (arr[5:8])
#[5 6 7]  左闭右开

arr[5:8]=12
print (arr)
#[ 0  1  2  3  4 12 12 12  8  9]

arr_copy = arr[0:3].copy()
print (arr_copy)
#[0 1 2]
arr_copy[:]=12 #切片[ : ]会给数组中的所有值赋值
print (arr_copy)
#[12 12 12]
print (arr)
#[ 0  1  2  3  4 12 12 12  8  9]

'''
如上所示，当你将一个标量值赋值给一个切片时（如arr[5:8]=12），
该值会自动传播（也就说后面将会讲到的“广播”）到整个选区。跟列表最重要的区别在于，
数组切片是原始数组的视图。这意味着数据不会被复制，视图上的任何修改都会直接反映到源数组上。

注意：如果你想要得到的是ndarray切片的一份副本而非视图，就需要明确地进行复制操作，例如arr[5:8].copy()。
'''
print ('-----------')


#二维数组
arr2d = np.array([[1,2,3],[4,5,6],[7,8,9]])
print (arr2d[2])
print (arr2d[1][2])
print (arr2d[1,2])
# [7 8 9]
# 6
# 6


arr3d = np.array([
    [[1,2,3],[4,5,6]],
    [[7,8,9],[10,11,12]]
])

print (arr3d)
# [[[ 1  2  3]
#   [ 4  5  6]]
#  [[ 7  8  9]
#   [10 11 12]]]

print (arr3d[0])
# [[1 2 3]
#  [4 5 6]]

old_values = arr3d[0].copy()
arr3d[0]=42
print (arr3d)
# [[[42 42 42]
#   [42 42 42]]
#  [[ 7  8  9]
#   [10 11 12]]]

arr3d[0]=old_values
print (arr3d)
# [[[ 1  2  3]
#   [ 4  5  6]]
#  [[ 7  8  9]
#   [10 11 12]]]

print (arr3d[1,0])
#[7 8 9]

print ('-----------')

'''
切片索引
'''
print (arr)
#[ 0  1  2  3  4 12 12 12  8  9]

print (arr[1:6])
#[ 1  2  3  4 12]

print (arr2d)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]

print (arr2d[:2])
# [[1 2 3]
#  [4 5 6]]

print (arr2d[:2,1:])
# [[2 3]
#  [5 6]]

#像这样进行切片时，只能得到相同维数的数组视图。通过将整数索引和切片混合，可以得到低维度的切片。
print (arr2d[1,:2])
#[4 5]
print (arr2d[:2,2])
#[3 6]
print (arr2d[:,:1])
# [[1]
#  [4]
#  [7]]
#对切片表达式的赋值操作也会被扩散到整个选区：
arr2d[:2,1:]=0
print (arr2d)
# [[1 0 0]
#  [4 0 0]
#  [7 8 9]]

print ('-----------')

'''
布尔型索引
使用&:和
|:或
~:反转条件
注意：Python关键字and和or在布尔型数组中无效。要使用&与|。
'''
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
data = np.random.randn(7, 4)
print (names=='Bob')
#[ True False False  True False False False]
print (data[names == 'Bob'])
# [[ 0.69925066 -0.52633212 -0.62884185  0.55769814]
#  [-0.47857101  0.00509345 -0.86011115  0.44381002]]

print ('-----------')

'''
数组转置和轴对换
转置是重塑的一种特殊形式，它返回的是源数据的视图（不会进行任何复制操作）。
数组不仅有transpose方法，还有一个特殊的T属性：
'''
arr=np.arange(15).reshape((3,5))
print (arr)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]]
print (arr.T)
# [[ 0  5 10]
#  [ 1  6 11]
#  [ 2  7 12]
#  [ 3  8 13]
#  [ 4  9 14]]

print ('-----------')

'''
4.2 通用函数：快速的元素级数组函数
通用函数（即ufunc）是一种对ndarray中的数据执行元素级运算的函数。
你可以将其看做简单函数（接受一个或多个标量值，并产生一个或多个标量值）的矢量化包装器。
'''
#一元（unary）ufunc

arr = np.arange(10)
print (arr)
#[0 1 2 3 4 5 6 7 8 9]
print (np.sqrt(arr))#开平方
# [0.         1.         1.41421356 1.73205081 2.         2.23606798
#  2.44948974 2.64575131 2.82842712 3.        ]
print (np.exp(arr))
# [1.00000000e+00 2.71828183e+00 7.38905610e+00 2.00855369e+01
#  # 5.45981500e+01 1.48413159e+02 4.03428793e+02 1.09663316e+03
#  # 2.98095799e+03 8.10308393e+03]

#二元ufunc
x=np.random.randn(8)
y=np.random.randn(8)
print (x)
# [ 0.6657792  -0.27375555 -0.96624584  0.82197669 -0.35608067  2.60162508
#  -0.11832585 -0.17568129]
print (y)
# [ 1.17478864  0.74919223 -0.14828051 -0.59350786  1.38522156 -2.22924579
#   0.79923967  0.35362729]
print (np.maximum(x,y)) #maximum计算了x和y中元素级别最大的元素
# [ 1.17478864  0.74919223 -0.14828051  0.82197669  1.38522156  2.60162508
#   0.79923967  0.35362729]

print ('-----------')

'''
4.3 利用数组进行数据处理
NumPy数组使你可以将许多种数据处理任务表述为简洁的数组表达式（否则需要编写循环）。
用数组表达式代替循环的做法，通常被称为矢量化
'''
#将条件逻辑表述为数组运算
#numpy.where函数是三元表达式x if condition else y的矢量化版本。假设我们有一个布尔数组和两个值数组：
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])
#假设我们想要根据cond中的值选取xarr和yarr的值：
#当cond中的值为True时，选取xarr的值，否则从yarr中选取。列表推导式的写法应该如下所示：
result = np.where(cond,xarr,yarr)
print (result)
#[1.1 2.2 1.3 1.4 2.5]

#假设有一个由随机数据组成的矩阵，你希望将所有正值替换为2，将所有负值替换为－2。
arr = np.random.randn(4, 4)
print (arr > 0)
print (np.where(arr>0,2,-2))
#使用np.where，可以将标量和数组结合起来。例如，我可用常数2替换arr中所有正的值：
print (np.where(arr > 0,2,arr))

print (arr)
#arr中第0列中数字大于0，第一列数字小于0，则为1，否则为0
result = np.where(((arr[:,0]>0) & (arr[:,1] < 0)),1,0)
print (result.shape)

print ('-----------')


'''
数学和统计方法
arr.mean(1)是“计算行的平均值”，arr.sum(0)是“计算每列的和”
cumsum和cumprod之类的方法则不聚合，而是产生一个由中间结果组成的数组
'''
arr = np.random.randn(3,2)
print (arr)
# [[ 2.38331796 -0.49661818]
#  [ 1.49619429 -1.62052501]
#  [ 0.56640748 -1.60556908]]

print (arr.mean())
#0.12053457720343823

print (np.mean(arr))
#0.12053457720343823

print (arr.sum())
#0.7232074632206293
print ('-----------')

#mean和sum这类的函数可以接受一个axis选项参数，用于计算该轴向上的统计值，最终结果是一个少一维的数组：
print (arr.mean(axis=1))#arr.mean(1)是“计算行的平均值”
#[ 0.94334989 -0.06216536 -0.5195808 ]

print (arr.sum(axis=0))#arr.sum(0)是“计算每列的和
#[ 4.44591974 -3.72271227]

arr = np.array([0,1,2,3,4,5,6,7])
print (arr.cumsum())
#[ 0  1  3  6 10 15 21 28]
print ('-----------')


'''
用于布尔型数组的方法
sum经常被用来对布尔型数组中的True值计数，
any用于测试数组中是否存在一个或多个True，
all则检查数组中所有值是否都是True，
any和all这两个方法也能用于非布尔型数组，所有非0元素将会被当做True
'''
arr = np.random.randn(10)
print (arr)
# [ 0.97669369 -0.80090342  0.72656566  0.59803704 -0.01428153 -0.15706909
#  -0.50465267 -1.20262026 -1.47823324  0.64887852]

print ((arr > 0).sum())
#4

bools = np.array([False,False,True,False])
print (bools.any())
#True

print (bools.all())
#False

print ('-----------')

'''
排序
sort(1):每行按照从小到大排列
sort(0):每列按照从小到大排列
'''
arr = np.arange(20,10,-2)
print (arr)
#[20 18 16 14 12]
arr.sort()
print (arr)
#[12 14 16 18 20]

arr = np.random.randn(3,2)
print (arr)
# [[ 0.09051643  1.18443754]
#  [ 0.50771895 -0.45615291]
#  [ 0.41338272  0.3330323 ]]
arr.sort(1)
print (arr)
# [[ 0.09051643  1.18443754]
#  [-0.45615291  0.50771895]
#  [ 0.3330323   0.41338272]]
arr.sort(0)
print (arr)
# [[-0.45615291  0.41338272]
#  [ 0.09051643  0.50771895]
#  [ 0.3330323   1.18443754]]

#计算数组分位数最简单的办法是对其进行排序，然后选取特定位置的值：
large_arr = np.arange(1000,0,-3)
large_arr.sort()
print (large_arr[int(0.05*len(large_arr))]) #5%
#49

print ('-----------')


'''
唯一化以及其它的集合逻辑
np.unique:用于找出数组中的唯一值并返回已排序的结果
np.in1d:用于测试一个数组中的值在另一个数组中的成员资格，返回一个布尔型数组
'''
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
print (np.unique(names))
#['Bob' 'Joe' 'Will']

ints = np.array([3,3,3,2,2,1,1,4,4])
print (np.unique(ints))
#[1 2 3 4]

values = np.array([6, 0, 0, 3, 2, 5, 6])
print (np.in1d(values,[2,3,6])) #value中的值是否在【2，3，6】中
#[ True False False  True  True False  True]

print ('-----------')
