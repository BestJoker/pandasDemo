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
ndarray是一个通用的同构数据多维容器，也就是说，其中的所有元素必须是相同类型的。
每个数组都有一个shape（一个表示各维度大小的元组）和一个dtype（一个用于说明数组数据类型的对象）
'''
print (data.shape)
print (data.dtype)
print ('-----------')

'''
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
