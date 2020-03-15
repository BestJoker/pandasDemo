import pandas as pd
import numpy as np
import os
import openpyxl
from datetime import datetime,date,timedelta


def initData(start_date,end_date,topic_dic):

    # 生成对应的结果列表（'是否为当日'，'时间'）
    orign_start_date = '2020-02-03 21:30'
    orign_end_date = '2020-02-04 01:00'
    series = pd.date_range(start=orign_start_date, end=orign_end_date, freq='T')
    result_df = pd.DataFrame(series, columns=['时间'])
    # 构建'日期筛选系列'和'时间'的序列
    result_df['日期筛选系列'] = (result_df['时间'].astype(str).str[0:11] > '2020-02-04')
    result_df['时间'] = result_df['时间'].astype(str).str[11:16]
    result_df['画图时间'] = result_df['时间'] + '分'
    out_result_df = result_df.copy()
    # print (result_df)

    #构建一个表格数据，映射日期和主题和topic以及起始时间，总时长
    info_series = pd.date_range(start=start_date,end=end_date,freq='D')
    info_df = pd.DataFrame(columns=['日期','主题','topic_id','开始时间','结束时间'])
    info_df['日期'] = info_series

    for x in list(pd.date_range(start=start_date,end=end_date)):
        #生成时间，就是表格名称
        dateStr = x.strftime('%m-%d')
        #生成表格路径
        PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(PROJECT_ROOT, '多人讨论-区分付费/多人讨论分钟跳失/')
        path = path + dateStr + '分钟跳失.xlsx'

        try:
            df = pd.read_excel(path)
        except IOError:
            print('没有找到文件，进行全部数据统计')
            # 则进行全部重新初始化
        else:
            df = pd.read_excel(path)
            #找到对应日期主题，根据主题筛选数据，由于主题中有【58天互动学习】
            topic = topic_dic[dateStr]
            df = df[df['主题名称::filter'].str.contains(topic)].reset_index(drop=True)
            # print ('主题是:%s' %topic)
            print (df.head(1))

            # 将时间一列拆分开
            df['日期筛选系列'] = df['分钟'].str[0:5] > df['the_day'].str[5:10]
            df['时间'] = df['分钟'].str[6:11]

            #开始处理信息
            #1.获取'主题', 'tipic_id', '开始时间', '结束时间', '总时长'
            info_df.loc[info_df['日期'] == x,'主题'] = topic
            info_df.loc[info_df['日期'] == x,'topic_id'] = df['topic_id'][0]
            # #创建一个临时排序完成的df
            temp_df = df.sort_values(by=['分钟'],ascending=True)['分钟']
            temp_df= temp_df.reset_index(drop=True)
            # #计算出开始和结束时间
            start_time = temp_df[0]
            end_time = temp_df[temp_df.shape[0]-1]
            info_df.loc[info_df['日期'] == x,'开始时间'] = start_time
            info_df.loc[info_df['日期'] == x,'结束时间'] = end_time

            #循环添加离开和加入类型人群
            for y in list(df['类型'].unique()):
                name = df['the_day'].str[5:10][0]+ y + '人数'
                df[name] = df[df['类型'] == y]['分钟人数']

                df1 = df[df['类型'] == y][['日期筛选系列','时间',name]]
                df1 = df1.sort_values(by=['日期筛选系列','时间'])

                #加入到结果里面
                if y == '进入':
                    result_df = pd.merge(result_df, df1, how='left', on=['日期筛选系列', '时间'])
                else:
                    out_result_df = pd.merge(out_result_df, df1, how='left', on=['日期筛选系列', '时间'])

    # print (result_df.head(50))
    # print (out_result_df.head(50))
    # print (info_df.head(50))
    # print (result_df.columns)
    # print (out_result_df.columns)

    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(PROJECT_ROOT, '多人讨论-区分付费/多人讨论分钟跳失/分钟数据汇总.xlsx')
    writer = pd.ExcelWriter(path)
    result_df.to_excel(excel_writer=writer, sheet_name='进入人数', index=None)
    out_result_df.to_excel(excel_writer=writer,sheet_name='离开人数',index=None)
    info_df.to_excel(excel_writer=writer,sheet_name='信息',index=None)
    writer.save()
    writer.close()