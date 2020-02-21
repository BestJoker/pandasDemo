import pandas as pd
import numpy as np
import os
import openpyxl
from datetime import datetime,date,timedelta

#生成对应的结果列表（'是否为当日'，'时间'）
series = pd.date_range(start='2020-02-03 21:00',end='2020-02-04 01:00',freq='T')
result_df = pd.DataFrame(series,columns=['时间'])
#构建'日期筛选系列'和'时间'的序列
result_df['日期筛选系列'] = (result_df['时间'].astype(str).str[0:11] > '2020-02-04')
result_df['时间'] = result_df['时间'].astype(str).str[11:16]
print (result_df)

#构建一个表格数据，映射日期和主题和topic以及起始时间，总时长

for x in list(pd.date_range(start='2020-02-03',end='2020-02-04')):
    #生成时间，就是表格名称
    dateStr = x.strftime('%m-%d')
    #生成表格路径
    path = '/Users/fujinshi/Desktop/' + dateStr + '分钟跳失.xlsx'
    df = pd.read_excel(path)
    print (df.head(10))
    print (df.columns)
    # 筛选出只有58天直播活动的
    df = df[df['主题名称::filter'].str.contains('【58天')]
    # 将时间一列拆分开
    df['日期筛选系列'] = df['分钟'].str[0:5] > df['the_day'].str[5:10]
    df['时间'] = df['分钟'].str[6:11]
    print (list(df['类型'].unique()))
    for x in list(df['类型'].unique()):
        name = df['the_day'].str[5:10][0]+ x + '人数'
        df[name] = df[df['类型'] == x]['分钟人数']
        df1 = df[df['类型'] == x][['日期筛选系列','时间',name]]
        df1 = df1.sort_values(by=['日期筛选系列','时间'])
        result_df = pd.merge(result_df, df1, how='left', on=['日期筛选系列', '时间'])

print (result_df.head(50))
