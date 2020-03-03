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


def barTest(df):
    size = 10
    y1 = [6, 5, 8, 5, 6, 6, 8, 9, 8, 10]
    y2 = [5, 3, 6, 4, 3, 4, 7, 4, 4, 6]
    y3 = [4, 1, 2, 1, 2, 1, 6, 2, 3, 2]
    x = np.arange(size)
    total_width, n = 0.8, 3
    width = total_width / n
    plt.bar(x,y1,width=width,color='r')
    plt.bar(x+width,y2,width=width,color='g')
    plt.bar(x+2*width,y3,width=width,color='b')
    plt.xticks(x+width,x)
    plt.xlabel('日期')
    plt.ylabel('数量')
    plt.title('标题')
    #显示应有的值
    for a,b in zip(x,y1):
        plt.text(a,b+0.1,b,ha='center',va='bottom')
    for a,b in zip(x,y2):
        plt.text(a+width,b+0.1,b,ha='center',va='bottom')
    for a, b in zip(x,y3):
        plt.text(a+2*width, b + 0.1,b, ha='center', va='bottom')

    plt.show()

def daysPie(df):
    print (df)
    df = df.set_index('次数')
    colors = ['peru','coral','salmon','yellow','grey']
    labels = np.array(df.columns)
    rations = np.array(df.loc['比例'].values)
    explode = [0.03,0.03,0.03,0.03,0.03]
    #绘制饼图
    plt.pie(rations,explode=explode,colors=colors,labels=labels,startangle=180,autopct='%.1f%%')
    plt.title('近五日留存')
    plt.axis('equal')#将饼图显示为正圆形
    plt.show()



count_df = pd.read_excel(path, sheet_name='主题维度分人群数据')
time_df = pd.read_excel(path,sheet_name='平均时长分布')
days_df = pd.read_excel(path,sheet_name='围观用户天数分布')
# onlooker_count(count_df,time_df)
# barTest(count_df)
daysPie(days_df)


