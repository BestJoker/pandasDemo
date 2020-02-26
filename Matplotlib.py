# coding:utf-8
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(PROJECT_ROOT,'多人讨论汇总数据.xlsx')

df = pd.read_excel(path)
print (df)
print (df.columns)

#总围观人数，社员围观人数曲线
plt.plot(df['日期'],df['总围观人数'])
plt.show()




