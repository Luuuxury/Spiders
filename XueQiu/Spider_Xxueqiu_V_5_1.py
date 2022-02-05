#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import json 
import warnings
import pandas as pd 
import pymysql
import tushare as ts

warnings.filterwarnings('ignore')


# # (#) Fetch all stock symbol
# 

# In[7]:


def Transfer_Ts_stock_code(ts_code_list):
    stock_code_list = ts_code_list
    stock_code_list_for_Xueqiu = []
    for stock_code in stock_code_list:
        num = stock_code.split('.')[0]
        exchange = stock_code.split('.')[1]
        stock_code_list_for_Xueqiu.append(exchange+num)
    return stock_code_list_for_Xueqiu


# In[8]:


ts.set_token('your token')
ts_api = ts.pro_api()   
Df_stocks_set = ts_api.query('stock_basic', exchange='', list_status='L',fields='ts_code')
stock_symbol_list = Transfer_Ts_stock_code(Df_stocks_set['ts_code'])


# # MySQL

# ## (#) init stock table

# In[9]:


def init_stock_table(stock_symbol_list, start_time):

    db = pymysql.connect(
        host='your ip',
        user='root',
        password='',
        database='XueQiu_Posts'
        )
    cursor = db.cursor()
    
    for stock_symbol in stock_symbol_list:
        sql_create_table = """
            CREATE TABLE `{}` (
            `Date` datetime(6) DEFAULT NULL,
            `User_ID` char(64) DEFAULT NULL,
            `Meme` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
            `Text` varchar(1024) CHARACTER SET utf8 DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""".format(stock_symbol)
        
        userid, meme, text =  12345, "[大笑]", "文本测试"
        sql_insert_init_data = """
            INSERT INTO `{}`(Date,
            User_ID, Meme, Text)
            VALUES ('{}', {}, '{}', '{}')""".format(stock_symbol, start_time, userid, meme, text)
        try:
            cursor.execute(sql_create_table)
            cursor.execute(sql_insert_init_data)
            return_info = cursor.fetchall()
            db.commit()
        except:
            db.rollback()
    db.close()


# In[16]:


# start_time = "2022-01-17 00:00:00"
# init_stock_table(stock_symbol_list, start_time)


# ## Fetch_all_table_name

# In[19]:


def Fetch_all_table_name():
    while True:
        try:
            db = pymysql.connect(
                host='your ip',
                user='root',
                password='your passed',
                database='XueQiu_Posts'
                )
            break
        except Exception as e:
            print(e)
            print("wait a second will re-connect")
            time.sleep(10)
            pass
        
    cursor = db.cursor() 
    
    sql = "show tables;"

    try:
        cursor.execute(sql)
        return_info = cursor.fetchall()
        table_name_list = []
        for i in return_info:
            table_name_list.append(i[0])
        db.commit()
    except:
        db.rollback()

    db.close()
    return table_name_list


# In[21]:


table_name_list = Fetch_all_table_name()
len(table_name_list)


# ## Fetch_latest_DateTime

# In[50]:


def Fetch_latest_DateTime(stock_symbol):
    while True:
        try:
            db = pymysql.connect(
                host='your ip ',
                user='root',
                password='your pass',
                database='XueQiu_Posts'
                )
            break
        except Exception as e:
            print(e)
            print("wait a second will re-connect")
            time.sleep(10)
            pass
    cursor = db.cursor()
    
    sql = "SELECT * FROM {} ORDER BY Date DESC LIMIT 1;".format(stock_symbol)

    try:
        cursor.execute(sql)
        return_info = cursor.fetchone()[0]
        db.commit()
    except:
        db.rollback()

    db.close()
    return return_info


# In[53]:


return_info = Fetch_latest_DateTime('SZ300750')
print(return_info) 


# ## Insert_Mysql

# In[49]:


def Insert_Mysql(stock_symbol, post_time, user_id, meme_list, post_content):
    while True:
        try:
            db = pymysql.connect(
                host='your ip',
                user='root',
                password='your passwd',
                database='XueQiu_Posts'
                ) 
            break
        except Exception as e:
            print(e)
            print("wait a second will re-connect")
            time.sleep(10)
            pass
        
    cursor = db.cursor()
    sql = """
        INSERT INTO `{}`(Date,
        User_ID, Meme, Text)
        VALUES ('{}', '{}', '{}', '{}')""".format(stock_symbol, post_time, user_id, meme_list, post_content)
    try:
        cursor.execute(sql)
        db.commit()
        print("{}-----写入Ok-----".format(post_time))
    except:
        db.rollback()

    db.close() 


# # Spider

# ## Fetch_sub_url

# In[54]:


def Fetch_sub_url(stock_symbol, page_num):
    headers = {"Refer": "https://xueqiu.com/k?q=%E9%99%90%E5%94%AE%E8%82%A1%E8%A7%A3%E7%A6%81",
               "Host": "xueqiu.com",
               "Cookie": "your Cookie",
               "User-Agent": '{}'.format(UserAgent().random),
               }
    while True:
        try:
            url = 'https://xueqiu.com/query/v1/symbol/search/status.json?count=10&comment=0&symbol={}&hl=0&source=all&sort=&page={}&q=&type=11'.format(stock_symbol, page_num)
            
            print("Layer-1, 开始请求: Fetch_sub_url", url)
            response = requests.get(url, headers=headers, verify=False, timeout=300)
            if response.status_code == 200:
                content = response.text 
                json_content = json.loads(content)
                json_list = json_content['list']
                return json_list
            elif response.status_code == 404:
                break
            else:
                print("Layer-1, 非200, 请求代码是 is {}, 等待重新请求 : {}".format(response.status_code, url))
                time.sleep(5)
                continue
        except Exception as e:
            print(e)
            print("Layer-1,报错 休息，继续")
            time.sleep(5)
            continue
        break 


# ## Fetch_one_Post_Content

# In[55]:


def Fetch_one_Post_Content(stock_symbol, sub_url, post_time):
    headers = {"Refer": "https://xueqiu.com/k?q=%E9%99%90%E5%94%AE%E8%82%A1%E8%A7%A3%E7%A6%81",
               "Host": "xueqiu.com",
               "Cookie": "your Cookie",
               "User-Agent": '{}'.format(UserAgent().random),
               }
    
    while True:
        try:
            full_post_url = "https://xueqiu.com" + sub_url
            print("Layer-2, 开始请求: Fetch_one_Post_Content", full_post_url)
            response = requests.get(full_post_url, headers=headers, timeout=300)
            response.encoding = response.apparent_encoding
            if response.status_code == 200:
                # print("Layer-2, 请求200 : {}".format(full_post_url))
                soup = BeautifulSoup(response.text)
                pattern = re.compile("article__bd__detail.*?")  # 按标签寻找
                page_info = soup.find_all("div", {'class': pattern})[0].get_text()

                user_id = int(page_info.split('com/')[1].split('/')[0])
                post_content = page_info.split("）")[1:]  # 这里的括号一定是中文的括号！
                post_content = "".join(post_content)
                
                images = soup.findAll('img')
                meme_list = []
                for image in images[1:]:
                    try:
                        image_meme = image['alt']
                        meme_list.append(image_meme)
                    except Exception as e:
                        continue
                meme_list = "".join(meme_list)
                # Go MySQL
                Insert_Mysql(stock_symbol, post_time, user_id, meme_list, post_content)
                break
            
            elif response.status_code == 404:
                break
            else:
                print("Layer-2, 非200/404，代码是 {} ，等待重新请求 {}".format(response.status_code, full_post_url)) 
                time.sleep(5)  
                continue
        except Exception as e:
            print(e)
            print("Layer-2, 报错，休息，继续")
            time.sleep(5)
            if "range" in str(e):
                break
            else:
                continue
        break  


# # Run Spider

# In[36]:


# Symbol_list = Fetch_all_table_name()
# len(Symbol_list)


# In[56]:


Symbol_list = Fetch_all_table_name()
for stock_symbol in Symbol_list:
# stock_symbol = ""
    print("============Now stock_symbol is {} =============".format(stock_symbol))
    symbol_break = 0
    only_run_once = 0
    for i in range(1, 101):
        json_list = Fetch_sub_url(stock_symbol, page_num=i)
        for json_meta in json_list:
            timestamp = int(json_meta['created_at'] / 1000)
            dateArray = datetime.utcfromtimestamp(timestamp) + timedelta(hours=8)
            post_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            sub_url = json_meta['target']

            if only_run_once == 0:
                latest_date = Fetch_latest_DateTime(stock_symbol)
                only_run_once = 1 
            else:
                pass

            if pd.to_datetime(post_time) > latest_date:
                while True:
                    try:
                        time.sleep(0.5)
                        Fetch_one_Post_Content(stock_symbol, sub_url, post_time)
                    except Exception as e:
                        print("Layer-3, 报错，休息继续")
                        print(e)
                        time.sleep(5)
                        continue
                    break
            else:
                symbol_break = 1
                print("----------------该Symbol的数据都爬过了，更换Symbol----------------")
                print("\n")
                time.sleep(0.5)
                break 
        if symbol_break == 1:
            break    


# # Tail
