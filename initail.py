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
    print (df.shape[0])
    print (df.columns)
    # 取出所有关于【58天直播】主题的内容
    df1 = df[df['主题'].str.startswith('【58天')]
    df1['reset_index'] = range(0,df1.shape[0])
    df1=df1.set_index(['reset_index'])
    print (df1)
    # 插入两列，用户身份和时长分布
    col_name = df1.columns.tolist()
    person_bool = '用户身份' in col_name
    time_bool = '时长分布' in col_name
    print (str(person_bool) + '和' + str(time_bool))
    if (person_bool & time_bool) == 1:
        print ('都有了')
    elif (person_bool == 0 and time_bool == 1):
        col_name.insert(4, '用户身份')
    elif (person_bool == 1 and time_bool == 0):
        print ('没有时长分布，增加')
        col_name.insert(5, '时长分布')
    elif (person_bool == 0 and time_bool == 0):
        col_name.insert(4, '用户身份')
        col_name.insert(5, '时长分布')
    df1 = df1.reindex(columns=col_name)
    print (df1.columns.tolist())

    # len(df1['用户创建时间'])
    for i in range(0, df1.shape[0]):  # len(df1['用户创建时间'])
        # 根据is_member和用户创建时间将用户分为社员，老注册和新注册三类
        orign_date_str = df1['用户创建时间'][i]
        date_str = orign_date_str.split('T')[0]
        if (df1['is_member'][i] == 1):
            df1.loc[i, '用户身份'] = '社员'
        elif date_str < '2020-02-01':
            df1.loc[i, '用户身份'] = '老注册'
        else:
            df1.loc[i, '用户身份'] = '新注册'

        # 根据用户观看时长，将将用户分为一个区间
        time = df1['围观时长(min)'][i]
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
        df1.loc[i, '时长分布'] = time_class_str

    print (df1[['用户ID', '用户身份', '时长分布']][0:100])
    # 判断过滤出来的主题是否唯一，如果不唯一，则分成两个列表
    list = df1['主题'].unique()
    # 生成excel的编辑器,拆解主题然后保存到对应额sheet中
    writer = pd.ExcelWriter(path)
    for i in range(0, len(list)):
        topic = list[i]  # 选出对应主题
        df2 = df1[df1['主题'] == topic]  # 将对应主题筛选出来
        df2.to_excel(excel_writer=writer, sheet_name=current_date_str + '-' + str(i), index=None)
    writer.save()
    writer.close()

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

dateStr = '02-24'
#生成表格路径
path = '/Users/fujinshi/Desktop/多人讨论/多人讨论围观明细数据/' + dateStr + '.xlsx'
print (path)
# 读取文件（文件夹中文件）
handing_excel(path,dateStr)

joiner_path = '/Users/fujinshi/Desktop/多人讨论/多人讨论上座明细/' + dateStr + '上座明细.xlsx'
# 读取文件（文件夹中文件）
handing_joiner_excel(joiner_path,dateStr)
