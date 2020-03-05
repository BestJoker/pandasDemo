# coding:utf-8
import pandas as pd
import numpy as np
import inout
import initail
import counting
from datetime import datetime,date,timedelta
import time

keep_days = 5
start_date = (date.today() + timedelta(days=-keep_days)).strftime("%Y-%m-%d")  # 昨天日期
end_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期

# #更新跳失人数
# inout.initData(start_date,end_date)
#
# #更新围观用户，上座用户
# initail.initData(start_date,end_date)

#延迟10s为了让前面的文件处理完成
time.sleep(3)

#计算综合数据
counting.initData(start_date,end_date,keep_days)

