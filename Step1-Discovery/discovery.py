#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import argparse
from time import time
from pathlib import Path
import pandas as pd     


# ## Read a file and display a few rows

# In[2]:


df = pd.read_csv('../data/turnstile_230603.csv.gz', iterator=False,compression="gzip")

# Check for null values in each column
null_counts = df.isnull().sum()
null_counts.head(5)

# fill null values with a specific value
df = df.fillna(0)


# In[3]:


df.info()


# ## Create a new DateTime column and merge the DATE and TIME columns

# In[4]:


# add the datetime column and drop the DATE and TIME columns
df['CREATED'] =  pd.to_datetime(df['DATE'] + ' ' + df['TIME'], format='%m/%d/%Y %H:%M:%S')
df = df.drop('DATE', axis=1).drop('TIME',axis=1)

df.head(5)


# ## Observations
# - ENTRIES are the departing commuters
# - EXITS are the arriving commuters
# - STATION provides the location
# 

# In[5]:


# clean the column names
df.columns = [column.strip() for column in df.columns]
print(df.columns)
df["ENTRIES"] = df["ENTRIES"].astype(int)
df["EXITS"] = df["EXITS"].astype(int)

# Aggregate the information by station and datetime
df_totals = df.groupby(["STATION","CREATED"], as_index=False)[["ENTRIES","EXITS"]].sum()
df_totals.head(5)


# In[28]:


df_station_totals = df.groupby(["STATION"], as_index=False)[["ENTRIES","EXITS"]].sum()
df_station_totals.head(10)


# ## Show the total entries by station, use a subset of data

# In[29]:


import plotly.express as px
import plotly.graph_objects as go
 
df_stations =  df_station_totals.head(25)

donut_chart = go.Figure(data=[go.Pie(labels=df_stations["STATION"], values=df_stations["ENTRIES"], hole=.2)])
donut_chart.update_layout(title_text='Entries Distribution by Station', margin=dict(t=40, b=0, l=10, r=10))
donut_chart.show()


# ## Show the data by the day of the week

# In[30]:


df_by_date = df_totals.groupby(["CREATED"], as_index=False)[["ENTRIES"]].sum()
day_order = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
df_by_date["WEEKDAY"] = pd.Categorical(df_by_date["CREATED"].dt.strftime('%a'), categories=day_order, ordered=True)
df_entries_by_date =  df_by_date.groupby(["WEEKDAY"], as_index=False)[["ENTRIES"]].sum()
df_entries_by_date.head(10)


# In[31]:


bar_chart = go.Figure(data=[go.Bar(x=df_entries_by_date["WEEKDAY"], y=df_entries_by_date["ENTRIES"])])
bar_chart.update_layout(title_text='Total Entries by Week Day')
bar_chart.show()

