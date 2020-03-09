# coding:utf-8
import pandas as pd
import numpy as np
import os
import openpyxl
from datetime import datetime,date,timedelta
import drawPic

#不同人群的观看人数和平均观看时长数据组合
def numExcelSheet(df,dateStr):
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
    # print ('日期' + ':' + date)
    # print ('主题' + ':' + topic)
    # print ('总围观人数' + ':' + str(total_num))
    # print ('社员围观人数' + ':' + str(member_num))
    # print ('老注册围观人数' + ':' + str(old_num))
    # print ('新注册' + ':' + str(new_num))
    # print ('总平均时长' + ':' + str(total_time))
    # print ('社员平均时长' + ':' + str(member_time))
    # print ('老注册平均时长' + ':' + str(old_time))
    # print ('新注册平均时长' + ':' + str(new_time))

    share_path = '/Users/fujinshi/Desktop/多人讨论-区分付费/多人讨论分享/' + dateStr + '分享.csv'
    joiner_path = '/Users/fujinshi/Desktop/多人讨论-区分付费/上座明细/' + dateStr + '上座.xlsx'
    all_share_num = 0
    joiner_share_num = 0
    onlooker_share_num = 0
    try:
        share_df = pd.read_csv(share_path)
        joiner_df = pd.read_excel(joiner_path)
    except IOError:
        print('没有找到文件')
    else:
        print ('可以执行')
        # 读取excel中原始数据
        share_df = pd.read_csv(share_path)
        joiner_df = pd.read_excel(joiner_path)
        share_id_df = share_df['登录 ID']
        joiner_id_df = joiner_df['用户ID']
        all_share_num = share_id_df.shape[0]
        result_share_df = pd.merge(share_df,joiner_id_df,left_on='登录 ID',right_on='用户ID',how='inner')
        joiner_share_num = result_share_df[result_share_df['登录 ID'] == result_share_df['用户ID']].shape[0]
        onlooker_share_num = all_share_num - joiner_share_num

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
        '新注册人均时长': new_time,
        '分享用户数':all_share_num,
        '上座用户数':joiner_share_num,
        '围观用户数':onlooker_share_num
    }
    new = pd.DataFrame(data, index=['0'])
    return new

#时长分布区间
def timeIntervalExcelSheet(df):
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
    total_5 = total_0_1+total_1_5
    total_30_up = total_30_60+total_60_90+total_90
    total_60_up = total_60_90+total_90
    total_5_rate = ((total_0_1+total_1_5) / total_num)
    total_10_rate = ((total_0_1+total_1_5+total_5_10) / total_num)
    total_30_up_rate = ((total_30_60+total_60_90+total_90) / total_num)


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
    member_5_rate = ((member_0_1+member_1_5) / member_num)
    member_10_rate = ((member_0_1+member_1_5+member_5_10) / member_num)
    member_30_up_rate = ((member_30_60+member_60_90+member_90) / member_num)

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
        '5分钟以内':total_5,
        '30分钟以上':total_30_up,
        '60分钟以上':total_60_up,
        '5分钟以内占比':total_5_rate,
        '10分钟以内占比':total_10_rate,
        '30分钟以上占比':total_30_up_rate,
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
        '社员90分钟以上': member_90,
        '社员5分钟以内占比':member_5_rate,
        '社员10分钟以内占比':member_10_rate,
        '社员30分钟以上占比':member_30_up_rate
    }
    new = pd.DataFrame(time_intercal_data, index=['0'])
    return new

#留存,df数据源，keep_df:保存不重复用户id，every_df:保存每一天的id
def keepExcelSheet(df,keep_series,every_df):
    keep_series = keep_series.append(df['用户ID'])


#处理分社分享数据
def community_share(topic_dic):
    # 多人讨论-分社看板_2020_03_05
    date_str = date.today().strftime('%Y_%m_%d')
    path = '/Users/fujinshi/Desktop/多人讨论-区分付费/多人讨论-分社看板_' + date_str + '.xlsx'
    df = pd.read_excel(path)
    # 先过滤出分社==全国的数据，在匹配主题
    df = df[df['分社'] == '全国'].reset_index(drop=True)
    # 主题进行分列，然后
    df['主题'] = df['主题'].str.split('】', expand=True)[1]
    # 匹配主题是否在主题字典中
    df = df[df['主题'].isin(topic_dic.values())]
    df = df.sort_values(by='日期').reset_index(drop=True)
    return df

# def initData(start_date,end_date,keep_days,topic_dic):
#
#     num_dataFrame = pd.DataFrame(
#         columns=['日期', '主题', '总围观人数', '社员围观人数', '老注册围观人数', '新注册围观人数', '总人均时长', '社员人均时长', '老注册人均时长', '新注册人均时长','分享用户数','上座用户数','围观用户数'])
#     print (num_dataFrame)
#
#     time_interval_dataFrame = pd.DataFrame(columns=['日期','总围观人数','1分钟以内','1~5分钟','5~10分钟','10~20分钟','20~30分钟','30~60分钟','60~90分钟','90分钟以上','5分钟以内','30分钟以上','60分钟以上','5分钟以内占比','10分钟以内占比','30分钟以上占比','---','社员日期','社员围观人数','社员1分钟以内','社员1~5分钟','社员5~10分钟','社员10~20分钟','社员20~30分钟','社员30~60分钟','社员60~90分钟','社员90分钟以上','社员5分钟以内占比','社员10分钟以内占比','社员30分钟以上占比'])
#     print (time_interval_dataFrame)
#
#     keep_series = pd.Series()#存放留存天数内所有用户ID，去重
#     dic = {}#存放每天访问用id，用户比较用户某天是否来过
#     time_list = list(pd.date_range(start=start_date, end=end_date))
#
#     #拿到现有的统计结果，如果有就进行赋值
#     result_path = '/Users/fujinshi/Desktop/多人讨论-区分付费/58天区分付费统计结果.xlsx'
#     try:
#         result_df = pd.ExcelFile(result_path)
#     except IOError:
#         print('没有找到文件，进行全部数据统计')
#         #则进行全部重新初始化
#     else:
#         print ('已经有现存文档，进行补充统计')
#         if '主题维度分人群数据' in result_df.sheet_names:
#             num_dataFrame = pd.read_excel(result_path,sheet_name='主题维度分人群数据')
#         if '平均时长分布' in result_df.sheet_names:
#             time_interval_dataFrame = pd.read_excel(result_path,sheet_name='平均时长分布')
#
#     for x in time_list:
#         # 生成时间，就是表格名称
#         dateStr = x.strftime('%m-%d')
#
#         # 生成表格路径
#         path = '/Users/fujinshi/Desktop/多人讨论-区分付费/围观明细/' + dateStr + '围观.xlsx'
#         # 判断如果没有文件则直接跳过，如果有文件则正常读取
#         try:
#             df = pd.read_excel(path)
#         except IOError:
#             print('没有找到文件')
#         else:
#             print ('可以执行')
#             # 读取excel中原始数据
#             df = pd.read_excel(path)
#
#         #日期
#         new_date_str = '2020-'+dateStr
#         num_array = np.array(num_dataFrame['日期'])
#         #如果历史的数据里面有对应日期，则不处理（暂时不考虑填充数据时候发生的异常）
#         if new_date_str in num_array:
#             print ('主题维度分人群数据「'+dateStr+'」已经有了，跳过')
#         else:
#             print ('主题维度分人群数据「'+dateStr+'」开始统计')
#             # 获取观看人数和时间的方法
#             new_num_df = numExcelSheet(df, dateStr)
#             # num_dataFrame存储的就是不同人群的观看人数和时长
#             num_dataFrame = num_dataFrame.append(new_num_df, ignore_index=True)
#
#         time_array = np.array(time_interval_dataFrame['日期'])
#         if new_date_str in time_array:
#             print ('平均时长分布「'+dateStr+'」已经有了，跳过')
#         else:
#             print ('平均时长分布「'+dateStr+'」开始统计')
#             #获取人均观看时长分段数据
#             new_time_interval_df = timeIntervalExcelSheet(df)
#             time_interval_dataFrame = time_interval_dataFrame.append(new_time_interval_df,ignore_index=True)
#
#         # 判断是否计算留存
#         keep_bool = 0
#         #如果list长度小于5天，则直接全部计算，如果大于则取后面5天
#         if (len(time_list) > keep_days):
#             if x in time_list[len(time_list) - keep_days:]:
#                 bool = 1
#             else:
#                 bool = 0
#         else:
#             bool = 1
#         #如果需要计算留存则计算，否则忽略
#         if bool==1:
#             #拼接找到所有用户ID，并且去重
#             keep_series = keep_series.append(df['用户ID'])
#             #去重
#             keep_series=keep_series.drop_duplicates()
#             dic[dateStr] = df['用户ID']
#
#
#     #根据保存的每天的记录，判断一个人在某天是否来了
#     #将用户去重数据填充到
#     every_df = pd.DataFrame({'用户ID':keep_series.values})
#     col_name = every_df.columns.tolist()
#
#     #日期中循环
#     for x in dic.keys():
#         if x in col_name:
#             print ('已经有%s列了' %x)
#             continue
#         else:
#             print ('没有%s列需要增加' %x)
#             col_name.insert(len(col_name),x)
#         every_df = every_df.reindex(columns=col_name)
#
#         for i in range(0,every_df['用户ID'].shape[0]):
#             id = every_df['用户ID'][i]
#             if id in dic[x].values:
#                 every_df.loc[i,x] = 1
#             else:
#                 every_df.loc[i,x] = 0
#
#     #由于地区不能参与运算, 因此在df1数据表中删除地区
#     every_df_drop = every_df.drop(['用户ID'], axis = 1, inplace = False)
#     #求每行的和，即为参加次数
#     every_df['参与次数'] = every_df_drop.apply(lambda x: x.sum(), axis=1)
#     #再根据分类计算分布
#     total_class_series = every_df['参与次数'].value_counts()
#
#     #创建一个时间分布的表格
#     join_count_df = pd.DataFrame(columns=['次数','人数','比例'])
#     #循环获取分布的数据，生成df，保存到表格中
#     for i in range(0,len(total_class_series.index)):
#         title = total_class_series.index.values[i]
#         num = total_class_series.values[i]
#         join_count_df.loc[i,'次数'] = str(title)+'天'
#         join_count_df.loc[i,'人数'] = num
#         join_count_df.loc[i,'比例'] = num / every_df['参与次数'].shape[0]
#
#     #全国分享数据
#     community_df = community_share(topic_dic)
#
#     print (num_dataFrame.tail(5))
#     print (time_interval_dataFrame.tail(5))
#     print (join_count_df.tail(5))
#     print (community_df.tail(5))
#     #为了防止有数据后续补充的，所以将数据按照日期进行重新排序
#     num_dataFrame = num_dataFrame.sort_values(by='日期',ascending=True)
#     time_interval_dataFrame = time_interval_dataFrame.sort_values(by='日期',ascending=True)
#
#     #直接生成对应excel
#     writer = pd.ExcelWriter(result_path)
#     num_dataFrame.to_excel(excel_writer=writer, sheet_name='主题维度分人群数据', index=None)
#     time_interval_dataFrame.to_excel(excel_writer=writer, sheet_name='平均时长分布', index=None)
#     join_count_df.T.to_excel(excel_writer=writer,sheet_name='围观用户天数分布')
#     community_df.to_excel(excel_writer=writer,sheet_name='分享数据')
#     writer.save()
#     writer.close()
#
#     # 将对应的文件画出来
#     drawPic.initData()

def initData(start_date,end_date,keep_days,topic_dic):

    num_dataFrame = pd.DataFrame(
        columns=['日期', '主题', '总围观人数', '社员围观人数', '老注册围观人数', '新注册围观人数', '总人均时长', '社员人均时长', '老注册人均时长', '新注册人均时长','分享用户数','上座用户数','围观用户数'])
    print (num_dataFrame)

    time_interval_dataFrame = pd.DataFrame(columns=['日期','总围观人数','1分钟以内','1~5分钟','5~10分钟','10~20分钟','20~30分钟','30~60分钟','60~90分钟','90分钟以上','5分钟以内','30分钟以上','60分钟以上','5分钟以内占比','10分钟以内占比','30分钟以上占比','---','社员日期','社员围观人数','社员1分钟以内','社员1~5分钟','社员5~10分钟','社员10~20分钟','社员20~30分钟','社员30~60分钟','社员60~90分钟','社员90分钟以上','社员5分钟以内占比','社员10分钟以内占比','社员30分钟以上占比'])
    print (time_interval_dataFrame)

    keep_series = pd.Series()#存放留存天数内所有用户ID，去重
    dic = {}#存放每天访问用id，用户比较用户某天是否来过
    time_list = list(pd.date_range(start=start_date, end=end_date))

    #拿到现有的统计结果，如果有就进行赋值
    result_path = '/Users/fujinshi/Desktop/多人讨论-区分付费/58天区分付费统计结果.xlsx'
    try:
        result_df = pd.ExcelFile(result_path)
    except IOError:
        print('没有找到文件，进行全部数据统计')
        #则进行全部重新初始化
    else:
        print ('已经有现存文档，进行补充统计')
        if '主题维度分人群数据' in result_df.sheet_names:
            num_dataFrame = pd.read_excel(result_path,sheet_name='主题维度分人群数据')
        if '平均时长分布' in result_df.sheet_names:
            time_interval_dataFrame = pd.read_excel(result_path,sheet_name='平均时长分布')

    for x in time_list:
        # 生成时间，就是表格名称
        dateStr = x.strftime('%m-%d')

        # 日期
        new_date_str = '2020-' + dateStr
        num_array = np.array(num_dataFrame['日期'])
        #用来判断是否需要读取文件
        num_bool = 0
        # 如果历史的数据里面有对应日期，则不处理（暂时不考虑填充数据时候发生的异常）
        if new_date_str in num_array:
            print ('主题维度分人群数据「' + dateStr + '」已经有了，跳过')
        else:
            print ('主题维度分人群数据「' + dateStr + '」开始统计')
            num_bool = 1

        # 用来判断是否需要读取文件
        time_bool = 0
        time_array = np.array(time_interval_dataFrame['日期'])
        if new_date_str in time_array:
            print ('平均时长分布「' + dateStr + '」已经有了，跳过')
        else:
            print ('平均时长分布「' + dateStr + '」开始统计')
            time_bool = 1

        if num_bool | time_bool:
            print ('需要读取文件')
            # 生成表格路径
            path = '/Users/fujinshi/Desktop/多人讨论-区分付费/围观明细/' + dateStr + '围观.xlsx'
            # 判断如果没有文件则直接跳过，如果有文件则正常读取
            try:
                df = pd.read_excel(path)
            except IOError:
                print('没有找到文件')
            else:
                print ('可以执行')
                # 读取excel中原始数据
                df = pd.read_excel(path)

            if num_bool:
                # 获取观看人数和时间的方法
                new_num_df = numExcelSheet(df, dateStr)
                # num_dataFrame存储的就是不同人群的观看人数和时长
                num_dataFrame = num_dataFrame.append(new_num_df, ignore_index=True)
            if time_bool:
                # 获取人均观看时长分段数据
                new_time_interval_df = timeIntervalExcelSheet(df)
                time_interval_dataFrame = time_interval_dataFrame.append(new_time_interval_df, ignore_index=True)
        else:
            print ('----------%s不需要读取文件，直接跳过' %dateStr)

        # 判断是否计算留存
        keep_bool = 0
        #如果list长度小于5天，则直接全部计算，如果大于则取后面5天
        if (len(time_list) > keep_days):
            if x in time_list[len(time_list) - keep_days:]:
                bool = 1
            else:
                bool = 0
        else:
            bool = 1
        #如果需要计算留存则计算，否则忽略
        if bool==1:
            #如果上面没有读取文件，你就自己读取文件，如果已经读取过了，就有df了
            if num_bool | time_bool == 0:
                path = '/Users/fujinshi/Desktop/多人讨论-区分付费/围观明细/' + dateStr + '围观.xlsx'
                # 判断如果没有文件则直接跳过，如果有文件则正常读取
                try:
                    df = pd.read_excel(path)
                except IOError:
                    print('没有找到文件')
                else:
                    print ('可以执行')
                    # 读取excel中原始数据
                    df = pd.read_excel(path)

            #拼接找到所有用户ID，并且去重
            keep_series = keep_series.append(df['用户ID'])
            #去重
            keep_series=keep_series.drop_duplicates()
            dic[dateStr] = df['用户ID']

    #根据保存的每天的记录，判断一个人在某天是否来了
    #将用户去重数据填充到
    every_df = pd.DataFrame({'用户ID':keep_series.values})
    col_name = every_df.columns.tolist()

    #日期中循环
    for x in dic.keys():
        if x in col_name:
            print ('已经有%s列了' %x)
            continue
        else:
            print ('没有%s列需要增加' %x)
            col_name.insert(len(col_name),x)
        every_df = every_df.reindex(columns=col_name)

        for i in range(0,every_df['用户ID'].shape[0]):
            id = every_df['用户ID'][i]
            if id in dic[x].values:
                every_df.loc[i,x] = 1
            else:
                every_df.loc[i,x] = 0

    #由于地区不能参与运算, 因此在df1数据表中删除地区
    every_df_drop = every_df.drop(['用户ID'], axis = 1, inplace = False)
    #求每行的和，即为参加次数
    every_df['参与次数'] = every_df_drop.apply(lambda x: x.sum(), axis=1)
    #再根据分类计算分布
    total_class_series = every_df['参与次数'].value_counts()

    #创建一个时间分布的表格
    join_count_df = pd.DataFrame(columns=['次数','人数','比例'])
    #循环获取分布的数据，生成df，保存到表格中
    for i in range(0,len(total_class_series.index)):
        title = total_class_series.index.values[i]
        num = total_class_series.values[i]
        join_count_df.loc[i,'次数'] = str(title)+'天'
        join_count_df.loc[i,'人数'] = num
        join_count_df.loc[i,'比例'] = num / every_df['参与次数'].shape[0]

    #全国分享数据
    community_df = community_share(topic_dic)

    print (num_dataFrame.tail(5))
    print (time_interval_dataFrame.tail(5))
    print (join_count_df.tail(5))
    print (community_df.tail(5))
    #为了防止有数据后续补充的，所以将数据按照日期进行重新排序
    num_dataFrame = num_dataFrame.sort_values(by='日期',ascending=True)
    time_interval_dataFrame = time_interval_dataFrame.sort_values(by='日期',ascending=True)

    #直接生成对应excel
    writer = pd.ExcelWriter(result_path)
    num_dataFrame.to_excel(excel_writer=writer, sheet_name='主题维度分人群数据', index=None)
    time_interval_dataFrame.to_excel(excel_writer=writer, sheet_name='平均时长分布', index=None)
    join_count_df.T.to_excel(excel_writer=writer,sheet_name='围观用户天数分布')
    community_df.to_excel(excel_writer=writer,sheet_name='分享数据')
    writer.save()
    writer.close()

    # 将对应的文件画出来
    drawPic.initData()