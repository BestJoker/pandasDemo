# coding:utf-8import pandas as pdimport numpy as npimport osimport openpyxlfrom datetime import datetime,date,timedelta#将每日的漏斗数据传入进来def get_total_data(df,array):    df['当日_时间'] = df['当日_时间'].str[5:10]    result_df = df[df['当日_分社'] == '全国'].sort_values(by='当日_时间',ascending=True).reset_index(drop=True)    result_df = result_df.set_index('当日_时间')    result_df = result_df[array]    #环比增长速度＝（本期数－上期数）/上期数*100％    df1 = result_df.iloc[-1::].reset_index(drop=True)    df2 = result_df.iloc[-2:-1:].reset_index(drop=True)    df3 = df1.sub(df2,fill_value = 0).div(df2).rename(index={0:'日环比'})    #拼接日环比    result_df = pd.concat([result_df,df3])    print (result_df)    return result_df#获取分社漏斗数据def get_community_data(df,sort_str):    end_date = (date.today() + timedelta(days=-1)).strftime("%m-%d")  # 昨天日期    #获取其中去除全国的分社数据，并且找到昨天的数据,并按照当天申请数量排序    result_df = df[(df['当日_分社'] != '全国') & (df['当日_时间'] == end_date)].sort_values(by=sort_str,ascending=False).reset_index(drop=True)    return result_dfdef begin():    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))    #处理漏斗数据    funnel_path = os.path.join(PROJECT_ROOT,'data/漏斗数据.xlsx')    funnel_df = pd.read_excel(funnel_path)    funnel_df = funnel_df.drop_duplicates(keep='first',inplace=False)    print (funnel_df.info())    funel_array = ['当日_已申请',                   '当日_已建立联系',                   '当日_已领取',                   '当日_建立联系转化率',                   '当日_领取转化率',                   '累计_已申请',                   '累计_已建立联系',                   '累计_已领取',                   '累计_建立联系转化率',                   '累计_领取转化率']    total_funnel_data_df = get_total_data(funnel_df,funel_array)    community_funnel_data_df = get_community_data(funnel_df,'当日_已申请')    #处理领取数据    learn_path = os.path.join(PROJECT_ROOT,'data/学习数据.xlsx')    learn_df = pd.read_excel(learn_path)    learn_df = learn_df.drop_duplicates(keep='first',inplace=False)    print (learn_df.head())    print (learn_df.info())    learn_array = ['当日_成功领取人数',                   '当日_新注册并领取人数',                   '当日_领取看课人数',                   '当日_新注册占比',                   '当日_上课转化率',                   '累计_成功领取人数',                   '累计_新注册并领取人数',                   '累计_领取看课人数',                   '累计_新注册占比',                   '累计_上课转化率']    total_learn_data_df = get_total_data(learn_df,learn_array)    comunity_learn_data_df = get_community_data(learn_df,'当日_成功领取人数')    result_path = os.path.join(PROJECT_ROOT,'data/日报汇总数据.xlsx')    writer = pd.ExcelWriter(result_path)    total_funnel_data_df.to_excel(excel_writer=writer,sheet_name='总体漏斗数据')    total_learn_data_df.to_excel(excel_writer=writer,sheet_name='总体学习数据')    community_funnel_data_df.to_excel(excel_writer=writer,sheet_name='分社漏斗数据',index=None)    comunity_learn_data_df.to_excel(excel_writer=writer,sheet_name='分社学习数据',index=None)    writer.save()    writer.close()begin()