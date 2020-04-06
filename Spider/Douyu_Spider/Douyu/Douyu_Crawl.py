import csv
import datetime
import time

import requests
from fake_useragent import UserAgent
import json

from lxml import etree

import requests

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HYT5TNXN21O664DD"
proxyPass = "173BD70958227720"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


headers = {"User-Agent": '{}'.format(UserAgent().random),
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-us",
           "Connection": "keep-alive",
           "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}



directory_url = 'https://www.douyu.com/directory'

Web = requests.get(directory_url, headers=headers, proxies=proxies).text

dom = etree.HTML(Web)

Game_urls_list = []
Game_names_list = []
for i in range(3, 13):
    Game_names = dom.xpath('//*[@id="allCate"]/section/div[{}]/ul/li/a/strong/text()'.format(i))
    Game_urls = dom.xpath('//*[@id="allCate"]/section/div[{}]/ul/li/a/@href'.format(i))

    for Gn in Game_names:
        Game_names_list.append(Gn)
    for Gu in Game_urls:
        G_url = Gu.split('_')[1]
        Game_urls_list.append(G_url)

All_game = dict(zip(Game_names_list, Game_urls_list))

    # print(Game_urls_list, All_game)

for G_name in All_game.keys():
    print("===========正在爬取========", G_name)
    count = 1
    for page in range(1, 350):
        # time.sleep(1)
        base_api = 'https://m.douyu.com/api/room/list?page={}&type={}'.format(page, All_game['{}'.format(G_name)])
        try:
            response = requests.get(base_api, headers=headers, proxies=proxies, timeout=30, verify=False).text

        except IOError:
            pass

        RoomList = json.loads(response).get('data').get('list')

        if len(RoomList) > 1:
            count += 1
            path = '/home/liuyang/Spider/Scrapy_Project/BS_Spider/Douyu/Info_Douyu2020-04-03-15:00.csv'
            # path = '/home/liuyang/Spider/Scrapy_Project/BS_Spider/Douyu/Douyu.csv'

            for room in RoomList:
                GameName = G_name
                RoomId = room.get('rid')
                RoomName = room.get('roomName')
                BlogName = room.get('nickname')
                HotSpots = room.get('hn')

                with open(path, "a+", encoding='utf-8-sig') as f:
                    writer = csv.writer(f, dialect="excel")
                    csv_write = csv.writer(f)
                    csv_data = [G_name, RoomId, RoomName, BlogName, HotSpots]
                    csv_write.writerow(csv_data)
                    f.close()
                    print(G_name, RoomId, RoomName, BlogName, HotSpots)
        else:
            count -= 10

        print(count, page)

        if count < page:
            break

