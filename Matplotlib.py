# coding:utf-8
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties

def getChineseFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(PROJECT_ROOT,'多人讨论汇总数据.xlsx')

df = pd.read_excel(path)
print (df)
print (df.columns)

###总围观人数，社员围观人数曲线

#两个参数，左边为x轴，右边为y轴
plt.plot(df['日期'],df['总围观人数'])
#横坐标变换45度
plt.xticks(rotation=45)
#设置坐标轴字体
plt.xlabel('日期',fontproperties=getChineseFont())
plt.ylabel('总围观人数',fontproperties=getChineseFont())
plt.title('总围观人数曲线',fontproperties=getChineseFont())
plt.show()





