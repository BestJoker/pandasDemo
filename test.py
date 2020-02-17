# coding:utf-8
import pandas as pd
import numpy as np
import os
import openpyxl


#读取文件（项目中文件）
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))#获取项目根目录
path = os.path.join(PROJECT_ROOT,"02-13多人讨论围观明细.xlsx") #文件路径

dateStr = '02-16'
#读取文件（文件夹中文件）
path = '/Users/fujinshi/Desktop/'+dateStr+'.xlsx'
print (path)
df = pd.read_excel(path)
print (df.shape)
print (df.columns)

#取出所有关于【58天直播】主题的内容
df1 = df[df['主题'].str.startswith('【58天')]
print (df1)

print (df1['用户创建时间'])
#插入两列，用户分类和时长分布
col_name = df1.columns.tolist()
print (col_name)
col_name.insert(4,'用户分类')
col_name.insert(5,'时长分布')
df1 = df1.reindex(columns=col_name)
print (df1.columns.tolist())
#len(df1['用户创建时间'])
for i in range(0,100):
    #根据is_member和用户创建时间将用户分为社员，老注册和新注册三类
    print (str(i)+'--'+df1['用户创建时间'][i]+'--'+str(df1['is_member'][i]))
    date_str = (df1['用户创建时间'][i].split('T'))[0]
    if (df1['is_member'][i] == 1):
        df1.loc[i, '用户身份'] = '社员'
    elif date_str < '2020-02-01':
        df1.loc[i, '用户身份'] = '老注册'
    else:
         df1.loc[i, '用户身份'] = '新注册'
    print (df1.loc[i, '用户身份'])
    #根据用户观看时长，将将用户分为一个区间
    


print (df1[['用户ID','用户身份']])

'''
#判断过滤出来的主题是否唯一，如果不唯一，则分成两个列表
list = df1['主题'].unique()
print (list[0])

#生成excel的编辑器,拆解主题然后保存到对应额sheet中
writer=pd.ExcelWriter(path)
for i in range(0,len(list)):
    topic = list[i]#选出对应主题
    df2 = df1[df1['主题'] == topic]#将对应主题筛选出来
    df2.to_excel(excel_writer=writer,sheet_name=dateStr+'-'+str(i),index=None)
writer.save()
writer.close()
'''


'''
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





