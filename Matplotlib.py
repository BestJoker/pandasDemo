# coding:utf-8
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MultipleLocator

#让中文显示正常
plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #用来正常显示中文标签字体。Microsoft YaHei 或 SimHei
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(PROJECT_ROOT,'58天区分付费统计结果.xlsx')

#绘制围观人数图像
def onlooker_count(count_df,time_df):

    plt.figure(figsize=(count_df['日期'].shape[0] / 1.2,15),dpi=80)

    #在创建规格为1x1的子图
    plt.subplot(2,1,1)

    print (count_df[['日期', '总围观人数']].head(10))
    print (count_df.columns)
    # 应该加一个判断，是否包含对应列，有问题则不处理

    # 生成对应的数据标签
    x = np.array(count_df['日期'])
    y = np.array(['总围观人数', '付费社员围观人数', '老注册围观人数', '新注册围观人数'])
    line_style_array = np.array(['r-', 'g-', 'b-', 'c-'])

    #创建曲线
    for i in range(0,y.size):
        x_str = y[i]
        plt.plot(count_df['日期'],count_df[x_str],line_style_array[i],label=y[i])

    plt.title('围观人数',verticalalignment='baseline')
    plt.yticks(np.arange(0,8000,1000))
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    # 添加图例
    plt.legend()

    for i in range(0,x.size):
        #获取对应横坐标
        a = x[i]
        for j in range(0,y.size):
            #获取对应标题，来去除对应纵坐标
            b = count_df[y[j]][i]
            plt.text(a, b + 0.3, '%d' % b, ha='center', va='bottom', fontsize=8)

    #添加围观人数分布图像
    plt.subplot(2, 2, 3)
    x = np.array(count_df['日期'])
    plt.bar(x, count_df['付费社员围观人数'], width=0.5, color='red', label='付费社员围观人数')
    plt.bar(x, count_df['老注册围观人数'], width=0.5, color='blue', label='老注册围观人数', bottom=count_df['付费社员围观人数'])
    plt.bar(x, count_df['新注册围观人数'], width=0.5, color='green', label='新注册围观人数', bottom=count_df['老注册围观人数'])
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    # 添加图例
    plt.legend()

    #添加30分钟，60分钟以上图像
    plt.subplot(2, 2, 4)
    y = np.array(['30分钟以上','60分钟以上'])
    line_style_array = np.array(['r-','b-'])
    #画图
    for i in range(0,y.size):
        str = y[i]
        plt.plot(time_df['日期'],time_df[str],line_style_array[i],label=y[i])
    #上数据标签
    for i in range(0,x.size):
        a = x[i]
        for j in range(0,y.size):
            #获取对应标题，来去除对应纵坐标
            b = time_df[y[j]][i]
            plt.text(a, b + 0.3, '%d' % b, ha='center', va='bottom', fontsize=8)
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.title('30分钟60分钟以上人数')
    #添加图例
    plt.legend()

    #保存图片
    plt.savefig('围观人数.png',dpi=150,bbox_inches='tight')
    plt.show()

def timePic(count_df,time_df,days_df):

    #构建画布
    plt.figure(figsize=(count_df['日期'].shape[0] / 1.2,15),dpi=80)

    #划分，绘制平均围观时长曲线
    plt.subplot(2,2,1)
    y = np.array(['总人均时长', '付费社员人均时长', '老注册人均时长', '新注册人均时长'])
    line_style_array = np.array(['r-', 'g-', 'b-', 'c-'])
    for i in range(len(y)):
        x_str = y[i]
        plt.plot(count_df['日期'],count_df[x_str],line_style_array[i],label=y[i])
    plt.title('平均围观时长')
    plt.xticks(rotation=45)
    plt.yticks(np.arange(0,70,10))
    plt.grid(axis='y')
    plt.legend()


    #绘制围观用户时长占比曲线
    plt.subplot(2,2,2)
    x = np.array(count_df['日期'])
    y = np.array(['5分钟以内占比','10分钟以内占比','30分钟以上占比'])
    line_style_array = np.array(['r-', 'g-', 'b-'])
    for i in range(len(y)):
        x_str = y[i]
        plt.plot(x,time_df[x_str],line_style_array[i],label=y[i])
    plt.title('总围观用户')
    plt.xticks(rotation=45)
    plt.yticks(np.arange(0,1,0.1))
    plt.grid(axis='y')
    plt.legend()
    #对应曲线赋值
    for i in range(len(x)):
        a = x[i]
        for j in range(len(y)):
            #获取对应标题，来去除对应纵坐标
            b = time_df[y[j]][i]
            plt.text(a, b + 0.005, '%1.1f' %(100*b)+'%', ha='center', va='bottom', fontsize=8)


    days_df = days_df.set_index('次数')
    labels = np.array(days_df.columns)
    rations = np.array(days_df.loc['比例'].values)
    counts = np.array(days_df.loc['人数'].values)

    # 绘制第一个柱状图
    plt.subplot(2, 2, 3)
    plt.bar(labels, counts, width=0.4, color='b')
    plt.grid(axis='y')
    plt.title('近5日留存人数')
    # 添加数据标签
    for a, b in zip(labels, counts):
        plt.text(a, b + 0.1, '%d' % b, ha='center', va='bottom')


    #绘制饼图
    plt.subplot(2,2,4)
    colors = ['b','r','g','y','c']
    explode = [0.03,0.03,0.03,0.03,0.03]
    #绘制饼图
    plt.pie(rations,explode=explode,colors=colors,labels=labels,startangle=180,autopct='%.1f%%',textprops={'color':'w',
                                                                                                           'fontsize':12})
    plt.title('近五日留存')
    plt.axis('equal')#将饼图显示为正圆形

    plt.show()

def scatterTest(df):
    #构建画布
    plt.figure(figsize=(8,5),dpi=80)
    x = np.random.normal(0, 1, 1000)  # 1000个点的x坐标
    y = np.random.normal(0, 1, 1000)  # 1000个点的y坐标
    c = np.random.rand(1000)  # 1000个颜色
    s = np.random.rand(100) * 100  # 100种大小
    plt.scatter(x, y, c=c, s=s, alpha=0.5)
    plt.grid(True)
    plt.show()

def subplotTest():
    fig = plt.figure()
    x = [1,2,3,4,5,6,7]
    y = [1,3,4,2,5,8,6]

    left,bottom,width,height = 0.1,0.1,0.8,0.8
    ax1 = fig.add_axes([left,bottom,width,height])
    ax1.plot(x,y,'r')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('title')

    ax2 = fig.add_axes([0.2,0.6,0.25,0.25])
    ax2.plot(y,x,'b')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title('title inside 1')

    plt.axes([0.6,0.2,0.25,0.25])
    plt.plot(y[::1],x,'g')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('title inside 2')
    plt.show()


count_df = pd.read_excel(path, sheet_name='主题维度分人群数据')
time_df = pd.read_excel(path,sheet_name='平均时长分布')
days_df = pd.read_excel(path,sheet_name='围观用户天数分布')
# onlooker_count(count_df,time_df)
# timePic(count_df,time_df,days_df)
# scatterTest(count_df)
subplotTest()
