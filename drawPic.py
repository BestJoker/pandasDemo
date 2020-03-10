# coding:utf-8import pandas as pdimport numpy as npimport osimport matplotlib.pyplot as pltimport matplotlibfrom matplotlib.font_manager import FontPropertiesfrom matplotlib.ticker import MultipleLocatorimport randomdef randomcolor():    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']    color = ""    for i in range(6):        color += colorArr[random.randint(0,14)]    return '#'+color#画围观人数分布曲线def drawNumPic(num_df,time_interval_df):    #创建画板    plt.figure(figsize=(num_df['日期'].shape[0] / 1.2,15),dpi=80)    #划分第一个区间    plt.subplot(2,1,1)    x = np.array(num_df['日期'])    title_array = np.array(['总围观人数','社员围观人数','老注册围观人数','新注册围观人数'])    color_array = np.array(['b','r','g','c'])    for i in range(len(title_array)):        columns_str = title_array[i]        plt.plot(x,num_df[columns_str],color=color_array[i],label=columns_str)    plt.title('围观人数')    #设置y的范围    plt.yticks(np.arange(0,8000,1000))    #设置x坐标旋转角度    plt.xticks(rotation=45)    #设置图例    plt.legend()    #网格线    plt.grid(axis='y')    for i in range(len(x)):        x_value = x[i]        for title in title_array:            y_value = num_df[title][i]            plt.text(x_value,y_value,y_value,ha='center',va='bottom',fontsize=14)    #构建围观人数百分比分布（柱状图）    plt.subplot(2,2,3)    plt.subplots_adjust(top=0.85)    title_array = np.array(['社员围观人数','老注册围观人数','新注册围观人数'])    rate_df = pd.DataFrame(columns=title_array)    rate_df['社员围观人数'] = num_df['社员围观人数'] / num_df['总围观人数']    rate_df['老注册围观人数'] = num_df['老注册围观人数'] / num_df['总围观人数']    rate_df['新注册围观人数'] = num_df['新注册围观人数'] / num_df['总围观人数']    plt.bar(x,rate_df['社员围观人数'],width=0.5,color='b',label='社员围观人数')    plt.bar(x,rate_df['老注册围观人数'],width=0.5,color='r',label='老注册围观人数',bottom=rate_df['社员围观人数'])    plt.bar(x,rate_df['新注册围观人数'],width=0.5,color='g',label='新注册围观人数',bottom=rate_df['老注册围观人数']+rate_df['社员围观人数'])    # for i in range(len(x)):    #     x_value = x[i]    #     #用来计算y坐标的    #     temp = 0    #     for j in range(len(title_array)):    #         title = title_array[j]    #         y_value = rate_df[title][i]    #         y_num = num_df[title][i]    #         plt.text(x_value, temp + y_value / 2, y_num, ha='center', va='bottom', fontsize=14)    #         temp = temp + y_value    plt.grid(axis='y')    plt.title('围观人数分布')    plt.xticks(rotation=45)    plt.legend(bbox_to_anchor=(1.02, 0), loc=3, borderaxespad=0)    #30分钟和60分钟以上曲线    plt.subplot(2,2,4)    plt.plot(x,time_interval_df['30分钟以上'],color='b',label='30分钟以上')    plt.plot(x,time_interval_df['60分钟以上'],color='r',label='60分钟以上')    plt.xticks(rotation=45)    plt.grid(axis='y')    plt.title('30分钟以上和60分钟以上')    plt.legend()    for i in range(len(x)):        x_value = x[i]        y1_value = time_interval_df['30分钟以上'][i]        y2_value = time_interval_df['60分钟以上'][i]        plt.text(x_value,y1_value+0.5,y1_value,ha='center',va='bottom',fontsize=14)        plt.text(x_value,y2_value+0.5,y2_value,ha='center',va='bottom',fontsize=14)    #保存图片    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))    root_path = os.path.join(PROJECT_ROOT, '多人讨论-区分付费/')    path = root_path + '围观人数.png'    plt.savefig(path,dpi=150,bbox_inches='tight')    print ('围观人数图片保存成功')    plt.show()def drawTimePic(num_df,time_interval_df,join_count_df):    plt.figure(figsize=(25,15),dpi=80)    #平均观看时长    plt.subplot(2,2,1)    title_array = np.array(['总人均时长','社员人均时长','老注册人均时长','新注册人均时长'])    color_array = np.array(['#6699FF','#FF6633','#009933','#993333'])    x = np.array(num_df['日期'])    #画曲线    for i in range(len(title_array)):        title = title_array[i]        plt.plot(x,num_df[title],color=color_array[i],label=title_array[i])    #上数据    for i in range(len(x)):        y = num_df['总人均时长'][i]        plt.text(x[i],y+0.5,y,ha='center',va='bottom',fontsize=8)    plt.xticks(rotation=45)    plt.title('平均围观时长')    plt.grid(axis='y')    plt.legend()    plt.subplot(2,2,2)    #总人数时长分布    time_title_array = np.array(['1分钟以内','1~5分钟','5~10分钟','10~20分钟','20~30分钟','30~60分钟','60~90分钟','90分钟以上'])    rate_df = pd.DataFrame(columns=time_title_array)    color_array = np.array(['#6699FF','#FF6633','#009933','#CC33CC','#3366FF','#FF9900','#993333','#FFCC33'])    for i in time_title_array:        rate_df[i] = time_interval_df[i] / time_interval_df['总围观人数']    for i in range(len(time_title_array)):        # 为了画图，在rate_df中增加一列bottom辅助列        rate_df['bottom'] = 0        time_title = time_title_array[i]        #计算当前的柱状图位置bottom        for j in range(i):            str = time_title_array[j]            rate_df['bottom'] = rate_df['bottom'] + rate_df[str]        #画图        plt.bar(x,rate_df[time_title],width=0.5,color=color_array[i],label=time_title_array[i],bottom=rate_df['bottom'])    plt.title('总人数时长分布')    plt.xticks(rotation=45)    plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)    #画柱状图    plt.subplot(2,2,3)    #取出其中有用的数据,变成多维数组    array = join_count_df.values[:,1:]    plt.bar(array[0],array[1],width=0.5,color='b')    for i in range(len(array[0])):        y = array[1][i]        plt.text(array[0][i],y,'%d' % y,ha='center',va='bottom')    plt.title('近5日留存人数')    #画百分比饼图    plt.subplot(2,2,4)    colors = ['b','r','g','y','c']    explode = [0.03,0.03,0.03,0.03,0.03]    plt.pie(array[2],labels=array[0],counterclock=False,startangle=90,autopct='%.1f%%',textprops={'color':'w','fontsize':12})    plt.title('近5日留存分布')    plt.legend()    plt.axis('equal')#将饼图显示为正圆形    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))    root_path = os.path.join(PROJECT_ROOT, '多人讨论-区分付费/')    path = root_path + '时长留存.png'    plt.savefig(path,dpi=150,bbox_inches='tight')    print ('时长留存图片保存成功')    plt.show()def initData():    # 让中文显示正常    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签字体。Microsoft YaHei 或 SimHei    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号    path = '/Users/fujinshi/Desktop/多人讨论-区分付费/58天区分付费统计结果.xlsx'    num_df = pd.read_excel(path,sheet_name='主题维度分人群数据')    time_interval_df = pd.read_excel(path,sheet_name='平均时长分布')    join_count_df = pd.read_excel(path,sheet_name='围观用户天数分布')    print (num_df.head(10))    print (time_interval_df.head(10))    print (join_count_df.head(10))    drawNumPic(num_df,time_interval_df)    drawTimePic(num_df,time_interval_df,join_count_df)