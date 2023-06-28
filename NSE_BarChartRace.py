#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests,csv
import bar_chart_race as bcr
import pandas as pd
from bs4 import BeautifulSoup


# In[2]:


nifty_list = ['HINDALCO','TATASTEEL','TATAMOTORS','JSWSTEEL','LT','TITAN','M&M','COALINDIA','BAJFINANCE','MARUTI','BHARTIARTL','GRASIM','RELIANCE','ASIANPAINT','HEROMOTOCO','BAJAJFINSV','TATACONSUM','HDFC','DIVISLAB','BAJAJ-AUTO','AXISBANK','NTPC','ADANIPORTS','ICICIBANK','ONGC','KOTAKBANK','SHREECEM','SBIN','DRREDDY','EICHERMOT','HDFCLIFE','UPL','BPCL','IOC','INDUSINDBK','ULTRACEMCO','HINDUNILVR','SUNPHARMA','WIPRO','HDFCBANK','CIPLA','POWERGRID','HCLTECH','SBILIFE','ITC','INFY','TCS','BRITANNIA','TECHM','NESTLEIND']


# In[3]:


url = 'https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36' , 'X-Requested-With': 'XMLHttpRequest' , 'Sec-Fetch-Site': 'same-origin', 'Host': 'www1.nseindia.com', 'Referer': 'https://www1.nseindia.com/products/content/equities/equities/eq_security.htm', 'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"', 'sec-ch-ua-mobile': '?0', 'Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive'}
param = {}
param['segmentLink'] = 3
param['series'] = 'EQ'
param['dateRange'] = '+'
param['fromDate'] = '23-03-2020'
param['toDate'] = '20-03-2021'
param['dataType'] = 'PRICEVOLUME'


# In[4]:


def rq_csv(param,headers):
    p = {'symbol':param['symbol']}
    param['symbolCount'] = requests.get("https://www1.nseindia.com/marketinfo/sym_map/symbolCount.jsp",p,headers=headers).content
    resp = requests.get(url,param,headers=headers,timeout=5)
    data = resp.content.strip()
    return data


# In[5]:


def shred(data):
    soup = BeautifulSoup(data, 'html.parser')
    dv = soup.find(id='csvContentDiv')
    s=dv.contents
    s=s[0]
    s = s.replace(':',',')
    s = s.replace('"','')
    s = s.replace(' ','')
    s = s.split(',')
    v = []
    dmy = []
    cnt = 0
    for it in s:
        dmy.append(it)
        cnt+=1
        if cnt == 13:
            cnt=0
            v.append(dmy)
            dmy=[]
    return v


# In[6]:


final_pd = pd.DataFrame()
flag = False
for index in nifty_list:
    param['symbol'] = index
    ls2d = shred(rq_csv(param,headers))
    prc = []
    dts = []
    for daily_prices in range(1,len(ls2d)):
        prc.append(float(ls2d[daily_prices][7]))
        if(flag == False):
            dts.append(ls2d[daily_prices][2])
    final_pd[index] = prc
    if(flag == False):
        final_pd.index=dts
    flag = True       


# In[7]:


final_pd.head()


# In[8]:


beg_dt = final_pd.loc['23-Mar-2020']
#beg_dt.head()
bgdt = beg_dt.values.tolist()
#print(bgdt)
r = final_pd.shape
for ri in range(r[0]):
    for ci in range(r[1]):
        final_pd.iat[ri,ci] = (final_pd.iat[ri,ci]/bgdt[ci])*10000
final_pd.head()


# In[9]:


bcr.bar_chart_race(df=final_pd,n_bars=10)
