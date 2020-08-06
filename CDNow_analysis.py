# coding:utf-8import pandas as pdimport numpy as npimport osimport matplotlib.pyplot as pltimport seaborn as snsimport datetimepd.options.mode.chained_assignment = None # 默认是'warn'plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #用来正常显示中文标签字体。Microsoft YaHei 或 SimHeiplt.rcParams['axes.unicode_minus']=False #用来正常显示负号'''一.处理数据，观察数据user_ud:用户IDorder_dt: 购买日期order_products: 购买产品数order_amount: 购买金额'''def get_oring_data():    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))    path = os.path.join(PROJECT_ROOT,'data/CDNOW_master.txt')    columns = ['user_id','order_dt','order_products','order_amount']    #\s+：匹配任意空白字符    orign_data = pd.read_csv(path, names=columns, sep='\s+')    #将日期转化为datetime格式    orign_data['order_dt'] = pd.to_datetime(orign_data.order_dt,format='%Y%m%d')    # 下面按照月份分析，所以需添加一个字段month，用它来表示订单日期所在的月份，格式为月份的第一天    # orign_data['month'] = orign_data['order_dt'].apply(lambda x:x.month)    orign_data['month'] = orign_data.order_dt.values.astype('datetime64[M]')    print (orign_data.head())    print (orign_data.info())    #没有缺失值,重复也正常    print (orign_data.groupby(by='user_id').sum().describe())    # 观察数据, 从用户ID看，每位用户平均购买7张CD，最多的用户购买了1033张，属于狂热用户了(观察异常值)。用户的平均消费金额（客单价）106    # 元，标准差是240，结合分位数和最大值看，平均值略大于第三分位数，肯定存在小部分的高额消费用户。    return orign_data'''二.数据分析'''# 1.按月分析用户消费趋势：每月消费总金额，每月订单数，每月消费产品购买量，每月用户数变化def analysis_1(df):    temp_df = df.copy()    grouped = temp_df.groupby(by='month')    fig = plt.figure(figsize=(25,15),dpi=80)    ax1 = fig.add_subplot(4,2,1)    ax2 = fig.add_subplot(4,2,3)    ax3 = fig.add_subplot(4,2,5)    ax4 = fig.add_subplot(4,2,7)    ax5 = fig.add_subplot(2,2,2)    ax6 = fig.add_subplot(2,2,4)    ax1.plot(grouped['order_amount'].sum(),color='blue')    ax1.set_title('每月消费总金额')    ax2.plot(grouped['order_products'].count(),color='red')    ax2.set_title('每月订单数')    ax3.plot(grouped['order_products'].sum(),color='green')    ax3.set_title('每月消费产品数量')    ax4.plot(grouped['user_id'].apply(lambda x:len(x.drop_duplicates())),color='black')    ax4.set_title('每月用户数变化')    ax5.plot(grouped['order_amount'].sum() / grouped['user_id'].apply(lambda x:len(x.drop_duplicates())),color='red')    ax5.set_title('每月用户消费的平均金额')    ax6.plot(grouped['order_products'].count() / grouped['user_id'].apply(lambda x:len(x.drop_duplicates())),color='blue')    ax6.set_title('每月用户消费的平均次数')    plt.show()    ##数据透视查看，按月分别对用户购买金额求和，订单数求和，用户人数计数    result_df = pd.pivot_table(temp_df,index='month',values=['order_amount','order_products','user_id'],aggfunc={'order_products':'sum','order_amount':'sum','user_id':'count'})# 2.用户个体消费分析def analysis_2(df):    temp_df = df.copy()    grouped_user = temp_df.groupby(by='user_id')    print (grouped_user.sum().describe())    #用户消费金额和消费次数散点图    plt.scatter(temp_df['order_amount'],temp_df['order_products'],s=5,alpha=0.5)    plt.title('订单散点图')    plt.grid(True)    plt.show()    # 每位用户的消费金额与消费商品数散点图,并用query过滤掉订单金额大于4000的订单，减小极值干扰    grouped_user.sum().query('order_amount<4000').plot.scatter(x='order_amount',y='order_products')    plt.show()    #用户消费金额的分布图(符合二八法则)    grouped_user.sum().order_amount.plot.hist(bins=20)    plt.show()    # 过滤掉商品数大于100的订单，减小极值影响，消费金额分布图    grouped_user.sum().query('order_products<100').order_amount.hist(bins=40)    plt.title('消费金额分布图')    plt.show()    # 按ID分组,并求和,再对订单金额进行排序(默认从小到大),最后通过匿名函数对每一行进行累计求和占比    print (grouped_user.sum().sort_values('order_amount'))    user_cumsum = grouped_user.sum().sort_values('order_amount').apply(lambda x:x.cumsum() / x.sum())    print (user_cumsum)    plt.subplot(211)    user_cumsum.reset_index().order_amount.plot(figsize=(8,8))    plt.title('消费金额累计百分比')    plt.grid()    plt.subplot(212)    user_cumsum.reset_index().order_products.plot()    plt.title('消费商品数累计百分比')    plt.grid()    plt.show()# 3. 用户消费行为分析def analysis_3(df):    temp_df = df.copy()    ##首次购买日分布    # temp_df.groupby(by='user_id')['order_dt'].min().value_counts().plot(figsize=(12,5))    # plt.show()    ##最后一次购买时间月分布    # temp_df.groupby(by='user_id')['month'].max().value_counts().plot()    # plt.show()    #新老客户消费比    # a.多少用户只消费一次    result_df = temp_df['user_id'].value_counts().reset_index()    rate = result_df[result_df['user_id'] == 1].shape[0] / result_df.shape[0]    print (rate)    # b.计算每月新客占比并作出其百分比折线图：    first = temp_df.groupby(by='user_id')['month'].min().value_counts()    total = temp_df['month'].value_counts()    result = pd.merge(total,first,left_index=True,right_index=True,how='left').sort_index(ascending=True)    result = result.fillna(value=0)    result['new_rate'] = result['month_y'] / result['month_x']    print (first)    print (total)    print (result)    plt.plot(result.index,result['new_rate'],color='b')    plt.show()# 4. 用户分层# R：消费最后一次消费时间的度量，数值越小越好# F：消费的总商品数，数值越大越好# M：消费的总金额，数值越大越好# 客户层次的定义,RFM得分可根据业务定义打分,也可以通过K-means聚类模型,得出不同相似程度的数据集,并且根据每一个数据集的特点进行客户定义def rfm_func(x):    level = x.apply(lambda x: '1' if x>=0 else '0')    #字符串拼接    # 111，R>0,是距离平均消费时间要久，R越大 说明没有消费时间越久  ，F >0 M>0,消费次数和金额也是较高的，重要价值客户，依次类推    label = level.R + level.F + level.M    d = {        '111': '重要价值客户',        '011': '重要保持客户',        '101': '重要挽留客户',        '001': '重要发展客户',        '110': '一般价值客户',        '010': '一般保持客户',        '100': '一般挽留客户',        '000': '一般发展客户'    }    result = d[label]    return result#RFM 拆分def analysis_4(df):    temp_df = df.copy()    rfm = temp_df.pivot_table(index='user_id',                              values=['order_products','order_amount','order_dt'],                              aggfunc={                                  'order_dt':'max',                                  'order_amount':'sum',                                  'order_products':'sum'                              })    # 计算每位用户最后一次消费时间与全部用户最后一次消费时间的差值    rfm['R'] = (rfm['order_dt']-rfm['order_dt'].max()).apply(lambda x:-x.days)    rfm.rename(columns={'order_amount':'M','order_products':'F'},inplace=True)    # 应用匿名函数,判断每一行值与平均值大小关系    rfm['label'] = rfm[['R','F','M']].apply(lambda x:x-x.mean()).apply(rfm_func,axis=1)    print (rfm)    # 计算每层客户R、F、M的和    print (rfm.groupby(by='label').sum())    #各类用户占比    user_c = rfm.groupby(by='label').count()    print (user_c)    labels = ['一般价值客户', '一般保持客户', '一般发展客户', '一般挽留客户', '重要价值客户', '重要保持客户', '重要发展客户', '重要挽留客户']    plt.pie(user_c['M'],            autopct='%3.1f%%',            labels = labels,            pctdistance=0.9,            labeldistance=1.2,            startangle=15            )    plt.show()# 用户购买周期(按订单)def analysis_5(df):    temp_df = df.copy()    # 计算用户相邻订单日期的差值,其中shift()函数是指将数据进行移动,默认axis=0    order_diff = temp_df.groupby(by='user_id').apply(lambda x:x.order_dt-x.order_dt.shift()).apply(lambda x:x.days)    order_diff.hist(bins=20)    plt.title('用户消费周期分布')    plt.show()    # 用户的生命周期受只购买一次的用户影响比较厉害（可以排除）    # 用户均消费134天，中位数仅0天，明显受到只购买一次用户的影响明显    # 用户生命周期分布    # usertime_diff代表用户消费首次订单与最后一次订单间隔时间    usertime_diff = temp_df.groupby('user_id')['order_dt'].max() - temp_df.groupby('user_id')['order_dt'].min()    usertime_diff = usertime_diff.apply(lambda x:x.days)    print (usertime_diff)    usertime_diff[usertime_diff>0].hist(bins=40)    plt.title('用户生命周期分布')    plt.show()# 6.复购率和回购率分析# 复购率:自然月内，购买多次的用户占比# 回购率:曾今购买过的用户在某一时期内的再次购买占比# 注:指标的定义和标准是根据不同公司的业务形态而变化def analysis_6(df):    temp_df = df.copy()    pivoted_counts = temp_df.pivot_table(index='user_id',                                         columns='month',                                         values='order_dt',                                         aggfunc='count').fillna(0)    print (pivoted_counts)    # 购买大于1次的 赋值为1 ，然后小于等于1 的 如果是购买次数是0，则赋值为空，否则 就是购买一次，赋值为0    purchase_r = pivoted_counts.applymap(lambda x:1 if x>1 else np.NaN if x == 0 else 0)    print (purchase_r)    # 计算复购率    print (purchase_r.sum() / purchase_r.count())    (purchase_r.sum() / purchase_r.count()).plot(figsize=(10,4))    plt.title('复购率')    plt.show()if __name__ == '__main__':    orign_df = get_oring_data()    analysis_6(orign_df)