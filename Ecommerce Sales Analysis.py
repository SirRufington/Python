#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# In[2]:


files=[file for file in os.listdir(r'C:\Users\ronfa\Desktop\Python Project\5-Sales Data Analysis\Sales_Data')]
for file in files:
    print(file)


# In[3]:


path=r'C:\Users\ronfa\Desktop\Python Project\5-Sales Data Analysis\Sales_Data'
all_data=pd.DataFrame()

for file in files:
    current_df=pd.read_csv(path+"/"+file)
    all_data=pd.concat([all_data,current_df])
    
all_data.shape


# In[4]:


all_data.to_csv(r'C:\Users\ronfa\Desktop\Python Project\5-Sales Data Analysis\Sales_Data/all_data.csv',index=False)


# In[5]:


all_data.head()


# In[6]:


## Data Cleaning
all_data.isnull().sum()


# In[7]:


all_data=all_data.dropna(how='all')
all_data.shape


# In[8]:


## Find out the Monthly Sales
'04/19/19 08:46'.split('/')[0]


# In[9]:


def month(x):
    return x.split('/')[0]


# In[10]:


all_data['month']=all_data['Order Date'].apply(month)


# In[11]:


all_data.head()


# In[12]:


all_data.dtypes


# In[13]:


all_data['month'].unique()


# In[14]:


filter=all_data['month']=='Order Date'
all_data=all_data[~filter]
all_data.head()


# In[15]:


all_data['month']=all_data['month'].astype(int)


# In[16]:


all_data.dtypes


# In[17]:


all_data['Quantity Ordered']=all_data['Quantity Ordered'].astype(int)
all_data['Price Each']=all_data['Price Each'].astype(float)


# In[18]:


all_data.dtypes


# In[19]:


all_data['sales']=all_data['Quantity Ordered']*all_data['Price Each']


# In[20]:


all_data.head()


# In[21]:


all_data.groupby('month')['sales'].sum()


# In[22]:


months=range(1,13)
plt.bar(months,all_data.groupby('month')['sales'].sum())
plt.xticks(months)
plt.xlabel('month')
plt.ylabel('Sales in USD')


# In[23]:


## Which city has maximum order
all_data.head()


# In[24]:


'917 1st St, Dallas, TX 75001'.split(',')[1]


# In[25]:


def city(x):
    return x.split(',')[1]


# In[26]:


all_data['city']=all_data['Purchase Address'].apply(city)


# In[27]:


all_data.head()


# In[28]:


all_data.groupby('city')['city'].count().plot.bar()


# In[29]:


## What time sales of products purchase is maximum
all_data['Order Date'].dtype


# In[30]:


all_data['Hour']=pd.to_datetime(all_data['Order Date']).dt.hour


# In[31]:


all_data.head()


# In[32]:


keys=[]
hour=[]
for key,hour_df in all_data.groupby('Hour'):
    keys.append(key)
    hour.append(len(hour_df))


# In[33]:


keys


# In[34]:


hour


# In[35]:


plt.grid()
plt.plot(keys,hour)
plt.xlabel('hour')


# In[36]:


## What product sold the most and why
all_data.groupby('Product')['Quantity Ordered'].sum().plot(kind='bar')


# In[37]:


all_data.groupby('Product')['Price Each'].mean()


# In[38]:


products=all_data.groupby('Product')['Quantity Ordered'].sum().index
quantity=all_data.groupby('Product')['Quantity Ordered'].sum()
prices=all_data.groupby('Product')['Price Each'].mean()


# In[39]:


fig,ax1=plt.subplots()
ax2=ax1.twinx()
ax1.bar(products,quantity,color='g')
ax2.plot(products,prices)
ax1.set_xticklabels(products,rotation='vertical',size=8)


# In[40]:


## What product is most sold together
all_data.head()


# In[41]:


df=all_data['Order ID'].duplicated(keep=False)
df2=all_data[df]
df2.head()


# In[42]:


df2['Grouped']=df2.groupby('Order ID')['Product'].transform(lambda x:','.join(x))


# In[43]:


df2.head()


# In[44]:


df2=df2.drop_duplicates(subset=['Order ID'])
df2.head()


# In[49]:


df2['Grouped'].value_counts()[0:5].plot.pie()
plt.ylabel('Group sales')

