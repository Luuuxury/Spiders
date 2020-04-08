#!/usr/bin/env python
# coding: utf-8

# In[3]:


import csv
import pandas as pd
data = pd.read_csv("Info_Douyu2020-04-07-12:00.csv")
data.info()


# In[4]:


pd.set_option('display.max_columns', None)  # 显示所有行
pd.set_option('display.max_rows', None)  # 显示所有行
G_count = data['G_name'].value_counts().to_frame().reset_index()
G_count.columns=["G_name", "count"]
G_count.sort_values('G_name')


# In[5]:


Hp_sum = data.groupby('G_name')
Hp_sum = Hp_sum['HotPoint'].sum().to_frame().reset_index()
Hp_sum.sort_values('G_name')


# In[6]:


G_H = pd.merge(Hp_sum, G_count).set_index('G_name')
G_H.sort_values('G_name')


# In[7]:


GH_average = (G_H["HotPoint"] / G_H["count"]).to_frame().reset_index()
GH_average.columns = ['G_name','Average']
GH_average


# In[8]:


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
plt.rc('font', family='SimHei', size=13)
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['figure.figsize'] = (400.0, 18.0)
plt.xticks(rotation=-45)
plt.bar(GH_average['G_name'], GH_average['Average'])
plt.title("平均热度")
plt.show()

