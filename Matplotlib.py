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

count_df = pd.read_excel(path, sheet_name='主题维度分人群数据')
time_df = pd.read_excel(path,sheet_name='平均时长分布')
onlooker_count(count_df,time_df)



