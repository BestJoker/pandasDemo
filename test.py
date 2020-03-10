# coding:utf-8
import pandas as pd
import numpy as np
import inout
import datetime
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(PROJECT_ROOT,'多人讨论-区分付费')
df = pd.read_excel(path+'/上座明细/03-09上座.xlsx')
