import csv
import requests
import json
import datetime
from datetime import timedelta
from fake_useragent import UserAgent


def gen_dates(start_date, day_counts):
    next_day = timedelta(days=1)  # timedalte 是datetime中的一个对象，该对象表示两个时间的差值,day=1表示相差一天
    for i in range(day_counts):  # 从起始时间的现在
        yield start_date + next_day * i


def get_date_list(start_date):
    """
    :param start_date: 开始时间
    :return: 开始时间未来40天后的日期列表
    """
    if start_date < datetime.datetime.now():
        start = datetime.datetime.now()
    else:
        start = start_date

    end = start + datetime.timedelta(days=40)  # 爬取未来一个月的机票
    data = []
    for d in gen_dates(start, ((end - start).days)):
        data.append(d.strftime("%Y-%m-%d"))
    return data


cities_data = [
    {"dcity": "SJW", "acity": "XMN", "dcityname": "石家庄", "acityname": "厦门", "date": "{}", "dcityid": 428, "token": "b2d909c0567e3327f371a22a241d6423"},
    {"dcity": "BJS", "acity": "XMN", "dcityname": "北京", "acityname": "厦门", "date": "{}", "dcityid": 1, "token": "aa7f5c829fcbdef594bbe797c45fa071"},
    {"dcity": "DLC", "acity": "XMN", "dcityname": "大连", "acityname": "厦门", "date": "{}", "dcityid": 6, "token": "f92a5202bc062161cd461898a81cc43e"},
    {"dcity": "CTU", "acity": "XMN", "dcityname": "成都", "acityname": "厦门", "date": "{}", "dcityid": 28, "token": "788dcce2c244858bfcf81d3484243bcd"},
    {"dcity": "SIA", "acity": "XMN", "dcityname": "西安", "acityname": "厦门", "date": "{}", "dcityid": 10, "token": "e1f5849e1aad88a7b9ab12530a0a0921"},
    {"dcity": "CKG", "acity": "XMN", "dcityname": "重庆", "acityname": "厦门", "date": "{}", "dcityid": 4, "token": "8c5b4af9edbbe4da52e2a2ceefbed1df"},
    {"dcity": "TAO", "acity": "XMN", "dcityname": "青岛", "acityname": "厦门", "date": "{}", "dcityid": 7, "token": "b3386e6b57fb4dcdceb135ba711ec03a"},
    {"dcity": "NKG", "acity": "XMN", "dcityname": "南京", "acityname": "厦门", "date": "{}", "dcityid": 12, "token": "67b9ba22590b5558696cb56acdf5f963"},
    {"dcity": "CSX", "acity": "XMN", "dcityname": "长沙", "acityname": "厦门", "date": "{}", "dcityid": 206, "token": "9747e71b8eb99cbe30ed8d1992a229c5"},
    {"dcity": "KMG", "acity": "XMN", "dcityname": "昆明", "acityname": "厦门", "date": "{}", "dcityid": 34, "token": "57763bd879e346496d1980d0a09cf3e1"},
    {"dcity": "TSN", "acity": "XMN", "dcityname": "天津", "acityname": "厦门", "date": "{}", "dcityid": 3, "token": "1da1b7fd1e67b73344b427c4f1725e7f"},
    {"dcity": "CGO", "acity": "XMN", "dcityname": "郑州", "acityname": "厦门", "date": "{}", "dcityid": 559, "token": "00b7d348881c750a3c40dc48975e8ade"},
    {"dcity": "TNA", "acity": "XMN", "dcityname": "济南", "acityname": "厦门", "date": "{}", "dcityid": 144, "token": "eb6685d9b7564f27b2261d1e6f062a03"},
    {"dcity": "SHE", "acity": "XMN", "dcityname": "沈阳", "acityname": "厦门", "date": "{}", "dcityid": 451,"token": "c59941ab1271f5f9e6aee3784ea7d215"},
    {"dcity": "URC", "acity": "XMN", "dcityname": "乌鲁木齐", "acityname": "厦门", "date": "{}", "dcityid": 39,"token": "36427d8c38639a44a490d108f96b2dae"},
    {"dcity": "HRB", "acity": "XMN", "dcityname": "哈尔滨", "acityname": "厦门", "date": "{}", "dcityid": 5, "token": "e048188e0dc27a8c2dfc1b0c25536782"},
    {"dcity": "HET", "acity": "XMN", "dcityname": "呼和浩特", "acityname": "厦门", "date": "{}", "dcityid": 103, "token": "48e57bfbcd9d3ae954d73422b8aa2d8c"}
    ]



if __name__ == "__main__":
    start_date = datetime.datetime.strptime("2020-03-30", "%Y-%m-%d")  # <class 'datetime.datetime'>
    date_data = get_date_list(start_date)
    for city_data in cities_data:
        for day in date_data:
            # url = "https://flights.ctrip.com/itinerary/api/12808/products/oneway/sjw,sjw-xmn?date={}".format(day)
            url = "https://flights.ctrip.com/itinerary/api/12808/products/oneway/{},{}-xmn?date={}".format(city_data.get('dcity'),
                                                                                                           city_data.get('dcity'),
                                                                                                           day)
            # 这里的url 必须写全！！！不能只写个path

            headers = {
                'User-Agent': '{}'.format(UserAgent().random),
                'Referer': 'https://flights.ctrip.com/itinerary/oneway/{},{}-xmn?date={}'.format(city_data.get('dcity'),
                                                                                                 city_data.get('dcity'),
                                                                                                 day),
                "Content-Type": "application/json"
            }

            request_payload = {
                "flightWay": "Oneway",
                "classType": "ALL",
                "hasChild": False,
                "hasBaby": False,
                "searchIndex": 1,
                "airportParams": [
                    {"dcity": "{}".format(city_data.get('dcity')),
                     "acity": "XMN",
                     "dcityname": "{}".format(city_data.get('dcityname')),
                     "acityname": "厦门",
                     "date": "{}".format(day),
                     "dcityid": "{}".format(city_data.get('dcityid'))}
                ],
                "token": "{}".format(city_data.get('token'))
            }

            # post请求
            response = requests.post(url, data=json.dumps(request_payload), headers=headers, timeout=10).text
            #  json.dumps 将 Python 对象编码成 JSON 字符串
            routeList = json.loads(response).get('data').get('routeList')  # 字典 get('key') 返回 value
            # json.loads 将已编码的 JSON 字符串解码为 Python 对象
            # 依次读取每条信息
            for route in routeList:
                # 判断是否有信息，有时候没有会报错
                if len(route.get('legs')) == 1:
                    legs = route.get('legs')
                    flight = legs[0].get('flight')
                    # 提取想要的信息
                    airlineName = flight.get('airlineName')
                    flightNumber = flight.get('flightNumber')
                    craftTypeName = flight.get('craftTypeName')

                    departureCityName = flight.get('departureAirportInfo').get('cityName')
                    departureAirportName = flight.get('departureAirportInfo').get('airportName')
                    departureterminal = flight.get('departureAirportInfo').get('terminal').get('name')
                    departureDate = flight.get('departureDate')

                    arrivalCityName = flight.get('arrivalAirportInfo').get('cityName')
                    arrivalAirportName = flight.get('arrivalAirportInfo').get('airportName')
                    arrivalterminal = flight.get('arrivalAirportInfo').get('terminal').get('name')
                    arrivalDate = flight.get('arrivalDate')

                    cabins = legs[0].get('cabins')[0]
                    price = cabins.get('price').get('price')

                    path = "/home/liuyang/Spider/Scrapy_Project/BS_Spider/Airtickets/TO_XMN{}.csv".format(start_date)

                    # 创建csv文件对象
                    with open(path, "a+", encoding='utf-8-sig') as f:
                        writer = csv.writer(f, dialect="excel")
                        # 基于文件对象构建 csv写入对象
                        csv_write = csv.writer(f)
                        csv_data = [airlineName, flightNumber,
                                    departureCityName, departureAirportName, departureterminal, departureDate,
                                    arrivalDate, arrivalCityName, arrivalAirportName, arrivalterminal,
                                    price, craftTypeName]
                        csv_write.writerow(csv_data)
                        f.close()

                    print(airlineName, "\t",
                          flightNumber, "\t",
                          price, "\t",
                          departureDate, "\t",
                          arrivalDate, "\t",
                          craftTypeName, "\t",
                          departureCityName, "\t",
                          departureAirportName, "\t",
                          departureterminal, "\t",
                          arrivalCityName, "\t",
                          arrivalAirportName, "\t",
                          arrivalterminal, )
                else:
                    pass
