# coding:utf-8
import pandas as pd
import numpy as np
import os
import openpyxl


#不同人群的观看人数和平均观看时长数据组合
def numExcelSheet(df):
    print (df.columns)
    # 获取不同用户群的数量
    print (df['用户身份'].shape[0])
    print (type(df['用户身份'].value_counts()))
    print (df['用户身份'].value_counts())
    # 获取不同用户身份的数量分布
    class_series = df['用户身份'].value_counts()
    date = df['日期'][0]
    topic = df['主题'][0]
    total_num = df['用户身份'].shape[0]
    member_num = class_series['社员']
    old_num = class_series['老注册']
    new_num = class_series['新注册']
    total_time = round(df['围观时长(min)'].mean() * 100) / 100.0
    member_time = round(df[df['用户身份'] == '社员']['围观时长(min)'].mean() * 100) / 100.0
    old_time = round(df[df['用户身份'] == '老注册']['围观时长(min)'].mean() * 100) / 100.0
    new_time = round(df[df['用户身份'] == '新注册']['围观时长(min)'].mean() * 100) / 100.0
    print ('日期' + ':' + date)
    print ('主题' + ':' + topic)
    print ('总围观人数' + ':' + str(total_num))
    print ('社员围观人数' + ':' + str(member_num))
    print ('老注册围观人数' + ':' + str(old_num))
    print ('新注册' + ':' + str(new_num))
    print ('总平均时长' + ':' + str(total_time))
    print ('社员平均时长' + ':' + str(member_time))
    print ('老注册平均时长' + ':' + str(old_time))
    print ('新注册平均时长' + ':' + str(new_time))
    data = {
        '日期': date,
        '主题': topic,
        '总围观人数': total_num,
        '社员围观人数': member_num,
        '老注册围观人数': old_num,
        '新注册围观人数': new_num,
        '总人均时长': total_time,
        '社员人均时长': member_time,
        '老注册人均时长': old_time,
        '新注册人均时长': new_time
    }
    new = pd.DataFrame(data, index=['0'])
    return new

#时长分布区间
def timeIntervalExcelSheet(df):
    print (type(df['时长分布'].value_counts()))
    print (df['时长分布'].value_counts())
    total_class_series = df['时长分布'].value_counts()
    date = df['日期'][0]
    total_num = df['时长分布'].shape[0]
    total_0_1 = total_class_series['1分钟以内']
    total_1_5 = total_class_series['1~5分钟']
    total_5_10 = total_class_series['5~10分钟']
    total_10_20 = total_class_series['10~20分钟']
    total_20_30 = total_class_series['20~30分钟']
    total_30_60 = total_class_series['30~60分钟']
    total_60_90 = total_class_series['60~90分钟']
    total_90 = total_class_series['90分钟以上']

    member_class_series = df[df['用户身份']=='社员']['时长分布'].value_counts()
    print (member_class_series)
    member_num = df[df['用户身份']=='社员']['时长分布'].shape[0]
    member_0_1 = member_class_series['1分钟以内']
    member_1_5 = member_class_series['1~5分钟']
    member_5_10 = member_class_series['5~10分钟']
    member_10_20 = member_class_series['10~20分钟']
    member_20_30 = member_class_series['20~30分钟']
    member_30_60 = member_class_series['30~60分钟']
    member_60_90 = member_class_series['60~90分钟']
    member_90 = member_class_series['90分钟以上']

    time_intercal_data = {
        '日期': date,
        '总围观人数': total_num,
        '1分钟以内': total_0_1,
        '1~5分钟': total_1_5,
        '5~10分钟': total_5_10,
        '10~20分钟': total_10_20,
        '20~30分钟': total_20_30,
        '30~60分钟': total_30_60,
        '60~90分钟': total_60_90,
        '90分钟以上': total_90,
        '---':'',
        '社员日期':date,
        '社员围观人数': member_num,
        '社员1分钟以内': member_0_1,
        '社员1~5分钟': member_1_5,
        '社员5~10分钟': member_5_10,
        '社员10~20分钟': member_10_20,
        '社员20~30分钟': member_20_30,
        '社员30~60分钟': member_30_60,
        '社员60~90分钟': member_60_90,
        '社员90分钟以上': member_90
    }
    print (date)
    new = pd.DataFrame(time_intercal_data, index=['0'])
    return new

#留存,df数据源，keep_df:保存不重复用户id，every_df:保存每一天的id
def keepExcelSheet(df,keep_series,every_df):
    print (type(df['用户ID']))
    print ('进入方法前')
    print (keep_series.shape)
    keep_series = keep_series.append(df['用户ID'])
    print ('拼接之后')
    print (keep_series.shape)


result_path = '/Users/fujinshi/Desktop/多人讨论数据.xlsx'

num_dataFrame = pd.DataFrame(
    columns=['日期', '主题', '总围观人数', '社员围观人数', '老注册围观人数', '新注册围观人数', '总人均时长', '社员人均时长', '老注册人均时长', '新注册人均时长'])
print (num_dataFrame)

time_interval_dataFrame = pd.DataFrame(columns=['日期','总围观人数','1分钟以内','1~5分钟','5~10分钟','10~20分钟','20~30分钟','30~60分钟','60~90分钟','90分钟以上','---','社员日期','社员围观人数','社员1分钟以内','社员1~5分钟','社员5~10分钟','社员10~20分钟','社员20~30分钟','社员30~60分钟','社员60~90分钟','社员90分钟以上'])
print (time_interval_dataFrame)

keep_series = pd.Series()
every_df = pd.DataFrame(columns=['用户ID'])

for x in list(pd.date_range(start='2020-02-03', end='2020-02-04')):
    # 生成时间，就是表格名称
    dateStr = x.strftime('%m-%d')
    # 生成表格路径
    path = '/Users/fujinshi/Desktop/多人讨论围测试明细/' + dateStr + '.xlsx'
    print (path)
    # 判断如果没有文件则直接跳过，如果有文件则正常读取
    try:
        df = pd.read_excel(path)
    except IOError:
        print('没有找到文件')
    else:
        print ('可以执行')
        # 读取excel中原始数据
        df = pd.read_excel(path)
        '''
        #获取观看人数和时间的方法
        new_num_df = numExcelSheet(df)
        num_dataFrame = num_dataFrame.append(new_num_df, ignore_index=True)
        #num_dataFrame存储的就是不同人群的观看人数和时长
        print (num_dataFrame)

        #获取人均观看时长分段数据
        new_time_interval_df = timeIntervalExcelSheet(df)
        time_interval_dataFrame = time_interval_dataFrame.append(new_time_interval_df,ignore_index=True)
        print (time_interval_dataFrame)

        writer = pd.ExcelWriter(result_path)
        num_dataFrame.to_excel(excel_writer=writer,sheet_name='主题维度分人群数据',index=None)
        time_interval_dataFrame.to_excel(excel_writer=writer,sheet_name='平均时长分布',index=None)
        writer.save()
        writer.close()
        '''
        #拼接找到所有用户ID，并且去重
        keep_series = keep_series.append(df['用户ID'])
        print (keep_series.shape)
        #去重
        keep_series=keep_series.drop_duplicates()
        print ('去重之后')
        print (keep_series.shape)

