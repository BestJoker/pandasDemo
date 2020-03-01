import pandas as pd
import numpy as np
import os
import openpyxl
from datetime import datetime,date,timedelta

def getTopicWithDateStr(dateStr):
    topic_dic ={
        '02-03': '疫情对你的工作生活产生了哪些问题和挑战？',
        '02-04': '疫情期间，我该如何合理规划开工节奏？',
        '02-05': '实体受困，如何单点破局实现业务转型？',
        '02-06': '哪些有意义的事情，让你打破了对疫情的焦虑？',
        '02-07': '零售等实体生意越来越难做，该怎么经营下去？',
        '02-08': '单点破局 | 疫情之后，职场人该如何提升核心能力？',
        '02-09': '困难时期，作为管理者的我，最应该做哪几件事？',
        '02-10': '自媒体时代，我们普通人如何打造个人超级IP?',
        '02-11': '2020年，中小企业如何找到新的增长点？',
        '02-12': '黑天鹅到来，如何从现有业务分形创新出新业务？',
        '02-13': '重口碑的教育培训行业，如何做营销才有效？',
        '02-14': '疫情之下，如何管理“个人现金流”？',
        '02-15': '如何利用深度思考解决复杂问题？',
        '02-16': '如果未来我们不属于任何一家公司，该如何做准备？',
        '02-17': '借鉴非典，零售人如何逆势增长？',
        '02-18': '特殊时期，品牌如何加强与用户的情感链接？',
        '02-19': '行业格局加速调整，你所在的企业如何突出重围？',
        '02-20': '高手是如何用OKR实现目标的？',
        '02-21': '怎样通过用户行为习惯读懂用户需求变化？',
        '02-22': '疫情影响下，如何用创新思维模型找到增长破局？',
        '02-23': '企业面临现金流大考，如何行动才能转危为安？',
        '02-24': '中美贸易战，对我们普通人有什么影响？',
        '02-25': '线上教育备受关注，如何借力新势能设计爆品课程？',
        '02-26': '疫情期间，企业如何挖掘颠覆创新的机会？',
        '02-27': '没有经验，怎样快速上手做短视频营销？',
        '02-28': '疫情过后，哪些方向更值得投资？',
        '02-29': '零售行业如何在疫情中寻找突破？'
    }
    topic = topic_dic[dateStr]
    return topic

#生成对应的结果列表（'是否为当日'，'时间'）
orign_start_date = '2020-02-03 21:30'
orign_end_date = '2020-02-04 01:00'
series = pd.date_range(start=orign_start_date,end=orign_end_date,freq='T')
result_df = pd.DataFrame(series,columns=['时间'])
#构建'日期筛选系列'和'时间'的序列
result_df['日期筛选系列'] = (result_df['时间'].astype(str).str[0:11] > '2020-02-04')
result_df['时间'] = result_df['时间'].astype(str).str[11:16]
result_df['画图时间'] = result_df['时间']+'分'
out_result_df = result_df.copy()
print (result_df)


#构建一个表格数据，映射日期和主题和topic以及起始时间，总时长
start_date = '2020-02-10'
end_date = '2020-02-29'
info_series = pd.date_range(start=start_date,end=end_date,freq='D')
info_df = pd.DataFrame(columns=['日期','主题','topic_id','开始时间','结束时间'])
info_df['日期'] = info_series

for x in list(pd.date_range(start=start_date,end=end_date)):
    #生成时间，就是表格名称
    dateStr = x.strftime('%m-%d')
    #生成表格路径
    path = '/Users/fujinshi/Desktop/多人讨论-区分付费/多人讨论分钟跳失/' + dateStr + '分钟跳失.xlsx'
    df = pd.read_excel(path)
    #找到对应日期主题，根据主题筛选数据，由于主题中有【58天互动学习】
    topic = getTopicWithDateStr(dateStr)
    df = df[df['主题名称::filter'].str.contains(topic)].reset_index(drop=True)
    # print ('主题是:%s' %topic)
    # print (df.head(2))

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

    if df['the_day'].str[5:10][0] == '02-22':
        print (df.head(10))

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


print (result_df.head(50))
print (out_result_df.head(50))
print (info_df.head(50))
print (result_df.columns)
print (out_result_df.columns)

path = '/Users/fujinshi/Desktop/多人讨论-区分付费/多人讨论分钟跳失/分钟数据汇总.xlsx'
writer = pd.ExcelWriter(path)
result_df.to_excel(excel_writer=writer, sheet_name='进入人数', index=None)
out_result_df.to_excel(excel_writer=writer,sheet_name='离开人数',index=None)
info_df.to_excel(excel_writer=writer,sheet_name='信息',index=None)
writer.save()
writer.close()
