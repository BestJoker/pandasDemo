# coding:utf-8import pandas as pdimport numpy as npimport osimport matplotlib.pyplot as pltimport seaborn as snsimport datetimepd.options.mode.chained_assignment = None # 默认是'warn'plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #用来正常显示中文标签字体。Microsoft YaHei 或 SimHeiplt.rcParams['axes.unicode_minus']=False #用来正常显示负号#https://zhuanlan.zhihu.com/p/41800432'''具体内容为：通过历史用车记录结合日期、天气、温湿度等等因素来预测共享单车项目在华盛顿的需求datetime(时间) - hourly date + timestampseason(季节) - 1 = spring, 2 = summer, 3 = fall, 4 = winterholiday(是否节日) - whether the day is considered a holidayworkingday(是否工作日) - whether the day is neither a weekend nor holidayweather(天气) -1: Clear, Few clouds, Partly cloudy, Partly cloudy清澈，少云，多云2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist雾+阴天，雾+碎云、雾+少云、雾3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds小雪、小雨+雷暴+散云，小雨+云4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog暴雨+冰雹+雷暴+雾，雪+雾temp(温度) - temperature in Celsiusatemp(体感温度) - "feels like" temperature in Celsiushumidity(湿度) - relative humiditywindspeed(风速) - wind speedcasual(临时用户) - number of non-registered user rentals initiatedregistered(注册用户) - number of registered user rentals initiatedcount(总租车数) - number of total rentals'''#获取原始训练数据def get_orign_df(file_name):    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))    path = os.path.join(PROJECT_ROOT,'data/bike-sharing-demand/'+file_name+'.csv')    orign_df = pd.read_csv(path)    print (orign_df.info())    print (orign_df.head())    return orign_df#处理数据def handle_data(train_df,test_df):    #1.处理count异常值    df = train_df.copy()    print (df.describe().T)    #这里可以看出count的标准差为181，几乎和平均值191相同了，而且75%分位数为284，最大值却为977，    #由此得出count的波动较大，我们详细看下count的密度分布    # f,ax = plt.subplots(figsize=(10,5))    # sns.distplot(df['count'])    # ax.set_title('Distribution of count')    # plt.show()    # 可以看到，count的密度分部为严重右偏，有一条很长的尾，我们将这个长尾进行处理，去除count的    # 3个标准差以外的数据    train_WithoutOutliers = df[np.abs(df['count']-df['count'].mean()) <= 3*df['count'].std()]    # f,ax = plt.subplots(figsize=(10,5))    # sns.distplot(train_WithoutOutliers['count'])    # ax.set_title('Distribution of count')    # plt.show()    #可以看出比先前稍微好了一点，但是数据波动还是太大，我们希望波动相对更加稳定：    #对数变换可以很好的处理自变量变大，因变量方差也变量的情况，所以我们选择使用对数变换来将数据进行处理    train_WithoutOutliers['count_log'] = np.log(train_WithoutOutliers['count'])    # sns.distplot(train_WithoutOutliers['count_log'])    # plt.title('Distribution of count after log')    # plt.show()    #可以看出，这里数据的波动已经相对 来说比较稳定，这样可以更好的进行后面的模型训练    #2.合并数据及处理    df = train_WithoutOutliers.append(test_df,ignore_index=True)    df = pd.DataFrame(df,columns=train_WithoutOutliers.columns)    print (df.head())    print (df.info())    return dfif __name__ == '__main__':#获取到原始数据    train_df = get_orign_df('train')    test_df = get_orign_df('test')    data_df = handle_data(train_df,test_df)