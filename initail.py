# coding:utf-8
import pandas as pd
import numpy as np
import os
import openpyxl
from datetime import datetime,date,timedelta

def getTopicWithDateStr(dateStr):
    topic_dic ={
        '02-03':'【58天互动学习场】疫情对你的工作生活产生了哪些问题和挑战？',
        '02-04': '【58天互动学习场】疫情期间，我该如何合理规划开工节奏？',
        '02-05': '【58天互动学习场】实体受困，如何单点破局实现业务转型？',
        '02-06': '【58天互动学习场】哪些有意义的事情，让你打破了对疫情的焦虑？',
        '02-07': '【58天互动学习场】零售等实体生意越来越难做，该怎么经营下去？',
        '02-08': '【58天互动学习场】单点破局 | 疫情之后，职场人该如何提升核心能力？',
        '02-09': '【58天互动学习场】困难时期，作为管理者的我，最应该做哪几件事？',
        '02-10': '【58天互动学习场】自媒体时代，我们普通人如何打造个人超级IP?',
        '02-11': '【58天互动学习场】2020年，中小企业如何找到新的增长点？',
        '02-12': '【58天互动学习场】黑天鹅到来，如何从现有业务分形创新出新业务？',
        '02-13': '【58天互动学习场】重口碑的教育培训行业，如何做营销才有效？',
        '02-14': '【58天互动学习场】疫情之下，如何管理“个人现金流”？',
        '02-15': '【58天互动学习场】如何利用深度思考解决复杂问题？',
        '02-16': '【58天互动学习场】如果未来我们不属于任何一家公司，该如何做准备？',
        '02-17': '【58天互动学习场】借鉴非典，零售人如何逆势增长？',
        '02-18': '【58天互动学习场】特殊时期，品牌如何加强与用户的情感链接？',
        '02-19': '【58天互动学习场】行业格局加速调整，你所在的企业如何突出重围？',
        '02-20': '【58天互动学习场】高手是如何用OKR实现目标的？',
        '02-21': '【58天互动学习场】怎样通过用户行为习惯读懂用户需求变化？',
        '02-22': '【58天互动学习场】传统企业进行数字化转型升级，如何避免踩坑？',
        '02-23': '【58天互动学习场】企业面临现金流大考，如何行动才能转危为安？',
        '02-24': '【58天互动学习场】中美贸易战，对我们普通人有什么影响？',
        '02-25':'【互动学习场】 线上教育备受关注，如何借力新势能设计爆品课程？'
    }
    topic = topic_dic[dateStr]
    return topic


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

def handing_excel(path,current_date_str):
    #判断如果没有文件则直接跳过，如果有文件则正常读取
    try:
        df = pd.read_excel(path)
    except IOError:
        print('没有找到文件')
        return
    else:
        print ('可以执行')

    #读取excel中原始数据
    df = pd.read_excel(path)
    print (df.head(15))
    print ('-'*10)

    # 取出所有关于互动学习主题的内容
    topic = getTopicWithDateStr(dateStr)
    df1 = df[df['主题']==topic]
    print (df1.head(10))
    print ('-'*30)

    #根据userid分类，然后计算用户的总时长
    df2 = df1.groupby(by=['用户ID']).agg({'围观时长(min)':'sum'})
    df2 = df2.reset_index()
    print (df2.head(5))
    print (df2.shape)
    #扔掉其他不需要的数据，并且去掉用户ID重复项
    df1.drop(['房间ID','房间','房主','围观时长(min)'],axis=1,inplace=True)
    df1.drop_duplicates(subset=['用户ID'], keep='first', inplace=True)
    #合并
    data = pd.merge(df1, df2, on='用户ID', how='left')
    print (data.head(10))
    print (data.columns)
    print (data.shape)

    print (data.columns.values)
    if '用户身份' in data.columns.values:
        if data['用户身份'].shape[0] != data.shape[0]:
            print ('用户身份有残缺')
            data['用户身份'] = df.apply(lambda row: getUserIdentityStr(row['is_member'], row['用户创建时间']), axis=1)
            print (data['用户身份'].value_counts())
        else:
            print ('已经处理过用户身份了')
    else:
        #处理用户分布
        print ('需要增加用户身份列')
        data['用户身份'] = df.apply(lambda row:getUserIdentityStr(row['is_member'],row['用户创建时间']),axis=1)
        print (data['用户身份'].value_counts())

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
        print (data['时长分布'].value_counts())

    print (data.head(10))

    # # 生成excel的编辑器,拆解主题然后保存到对应额sheet中
    writer = pd.ExcelWriter(path)
    data.to_excel(excel_writer = writer,sheet_name = topic,index=None)
    writer.save()
    writer.close()
    print ('保存成功')

def handing_joiner_excel(path,current_date_str):
    # 判断如果没有文件则直接跳过，如果有文件则正常读取
    try:
        df = pd.read_excel(path)
    except IOError:
        print('没有找到文件')
        return
    else:
        print ('可以执行')
    df = pd.read_excel(path)
    topic = getTopicWithDateStr(current_date_str)
    df = df[df['主题'] == topic]
    writer = pd.ExcelWriter(path)
    df.to_excel(excel_writer = writer,sheet_name = current_date_str,index=None)
    writer.save()
    writer.close()

# for x in list(pd.date_range(start='2020-02-20',end='2020-02-23')):
#     #生成时间，就是表格名称
#     dateStr = x.strftime('%m-%d')

dateStr = '02-25'
#生成表格路径
path = '/Users/fujinshi/Desktop/多人讨论-区分付费/围观明细/' + dateStr + '.xlsx'
print (path)
# 读取文件（文件夹中文件）
handing_excel(path,dateStr)

# joiner_path = '/Users/fujinshi/Desktop/多人讨论/多人讨论上座明细/' + dateStr + '上座明细.xlsx'
# # 读取文件（文件夹中文件）
# handing_joiner_excel(joiner_path,dateStr)
