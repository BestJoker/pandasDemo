# coding:utf-8
import pandas as pd
import numpy as np
import os
import openpyxl
from datetime import datetime,date,timedelta


def getUserIdentityStr(is_member,create_date):
    #转成字符串类型，避免有一些数据类型不正确
    create_date = str(create_date)
    create_date = create_date.split('T')[0]
    if is_member == 1:
        return '社员'
    elif create_date < '2020-02-01':
        return '老注册'
    else:
        return '新注册'

def getTime(time):
    time_class_str = ''
    if (time < 1):
        time_class_str = '1分钟以内'
    elif time < 5:
        time_class_str = '1~5分钟'
    elif time < 10:
        time_class_str = '5~10分钟'
    elif time < 20:
        time_class_str = '10~20分钟'
    elif time < 30:
        time_class_str = '20~30分钟'
    elif time < 60:
        time_class_str = '30~60分钟'
    elif time < 90:
        time_class_str = '60~90分钟'
    else:
        time_class_str = '90分钟以上'
    return time_class_str

def handing_excel(path,current_date_str,topic):
    #判断如果没有文件则直接跳过，如果有文件则正常读取
    try:
        df = pd.read_excel(path)
    except IOError:
        print('没有找到文件')
        return
    else:
        print ('可以执行')

    #判断是否处理过，如果处理过直接返回
    all_df = pd.read_excel(path,None)
    if '更新日期' in all_df.keys():
        current_df = all_df['更新日期']
        if current_df.size > 0:
            print (current_date_str+'日期已经更新过，跳过')
            return
        else:
            print ('异常：'+current_date_str+'日期有更新日期标题，但是没有内容，重新更新')

    #读取excel中原始数据
    df = pd.read_excel(path)
    #处理因为字段名称变更
    if '围观时长' in df.columns:
        df = df.rename(columns={'围观时长': '围观时长(min)'})

    print (df.head(5))
    # print ('-'*10)

    df1 = df[df['主题'].str.contains(topic)]
    print (df1.head(1))
    # print (df1.columns)
    # print ('-'*30)

    #根据userid分类，然后计算用户的总时长
    df2 = df1.groupby(by=['用户ID']).agg({'围观时长(min)':'sum'})
    df2 = df2.reset_index()

    #扔掉其他不需要的数据，并且去掉用户ID重复项
    df1.drop(['围观时长(min)'],axis=1,inplace=True)
    df1.drop_duplicates(subset=['用户ID'], keep='first', inplace=True)
    #合并
    data = pd.merge(df1, df2, on='用户ID', how='left')
    # print ('$'*30)
    # print (data.head(16))

    if '用户身份' in data.columns.values:
        if data['用户身份'].shape[0] != data.shape[0]:
            print ('用户身份有残缺')
            data['用户身份'] = df.apply(lambda row: getUserIdentityStr(row['is_member'], row['用户创建时间']), axis=1)
        else:
            print ('已经处理过用户身份了')
    else:
        #处理用户分布
        print ('需要增加用户身份列')
        data['用户身份'] = df.apply(lambda row:getUserIdentityStr(row['is_member'],row['用户创建时间']),axis=1)

    if '时长分布' in data.columns.values:
        if data['时长分布'].shape[0] != data.shape[0]:
            print ('用户身份有残缺')
            data['时长分布'] = df.apply(lambda row: getTime(row['围观时长(min)']), axis=1)
            print (data['时长分布'].value_counts())
        else:
            print ('已经处理过时长分布了')
    else:
        #处理用户分布
        print ('需要增加时长分布列')
        data['时长分布'] = df.apply(lambda row:getTime(row['围观时长(min)']),axis=1)

    # print (data.head(10))
    # print (data.columns)

    # 生成excel的编辑器,拆解主题然后保存到对应额sheet中
    writer = pd.ExcelWriter(path)
    data.to_excel(excel_writer = writer,sheet_name = current_date_str,index=None)
    #添加更新日期
    today_str = date.today().strftime("%Y-%m-%d")
    current_df = pd.DataFrame(data=[today_str],columns=['更新日期'])
    current_df.to_excel(excel_writer=writer,sheet_name='更新日期',index=None)
    writer.save()
    writer.close()

def handing_joiner_excel(path,current_date_str,topic):
    # 判断如果没有文件则直接跳过，如果有文件则正常读取
    try:
        df = pd.read_excel(path)
    except IOError:
        print('没有找到文件')
        return
    else:
        print ('可以执行')

    #判断是否处理过，如果处理过直接返回
    all_df = pd.read_excel(path,None)
    if '更新日期' in all_df.keys():
        current_df = all_df['更新日期']
        if current_df.size > 0:
            print (current_date_str+'日期已经更新过，跳过')
            return
        else:
            print ('异常：'+current_date_str+'日期有更新日期标题，但是没有内容，重新更新')

    df = pd.read_excel(path)
    df = df[df['主题'].str.contains(topic)]
    writer = pd.ExcelWriter(path)
    df.to_excel(excel_writer = writer,sheet_name=current_date_str,index=None)
    #添加更新日期
    today_str = date.today().strftime("%Y-%m-%d")
    current_df = pd.DataFrame(data=[today_str],columns=['更新日期'])
    current_df.to_excel(excel_writer=writer,sheet_name='更新日期',index=None)
    writer.save()
    writer.close()


def initail(dateStr,topic):
    # 生成表格路径
    path = '/Users/fujinshi/Desktop/多人讨论-区分付费/围观明细/' + dateStr + '围观.xlsx'
    print ('initail:' + path)
    # 读取文件（文件夹中文件）
    handing_excel(path, dateStr,topic)

    joiner_path = '/Users/fujinshi/Desktop/多人讨论-区分付费/上座明细/' + dateStr + '上座.xlsx'
    # 读取文件（文件夹中文件）
    handing_joiner_excel(joiner_path, dateStr,topic)


def initData(start_date,end_date,topic_dic):
    for x in list(pd.date_range(start=start_date, end=end_date)):
        # 生成时间，就是表格名称
        dateStr = x.strftime('%m-%d')
        topic = topic_dic[dateStr]
        initail(dateStr,topic)