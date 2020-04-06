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
    {"dcity": "SJW", "acity": "XMN", "dcityname": "石家庄", "acityname": "厦门", "date": "{}", "dcityid": 428, "token": "yourToken!"},
    {"dcity": "BJS", "acity": "XMN", "dcityname": "北京", "acityname": "厦门", "date": "{}", "dcityid": 1, "token": "yourToken!"},
    {"dcity": "DLC", "acity": "XMN", "dcityname": "大连", "acityname": "厦门", "date": "{}", "dcityid": 6, "token": "yourToken!"},
    {"dcity": "CTU", "acity": "XMN", "dcityname": "成都", "acityname": "厦门", "date": "{}", "dcityid": 28, "token": "yourToken!"},
    {"dcity": "SIA", "acity": "XMN", "dcityname": "西安", "acityname": "厦门", "date": "{}", "dcityid": 10, "token": "yourToken!"},
    {"dcity": "CKG", "acity": "XMN", "dcityname": "重庆", "acityname": "厦门", "date": "{}", "dcityid": 4, "token": "yourToken!"},
    {"dcity": "TAO", "acity": "XMN", "dcityname": "青岛", "acityname": "厦门", "date": "{}", "dcityid": 7, "token": "yourToken!"},
    {"dcity": "NKG", "acity": "XMN", "dcityname": "南京", "acityname": "厦门", "date": "{}", "dcityid": 12, "token": "yourToken!"},
    {"dcity": "CSX", "acity": "XMN", "dcityname": "长沙", "acityname": "厦门", "date": "{}", "dcityid": 206, "token": "yourToken!"},
    {"dcity": "KMG", "acity": "XMN", "dcityname": "昆明", "acityname": "厦门", "date": "{}", "dcityid": 34, "token": "yourToken!"},
    {"dcity": "TSN", "acity": "XMN", "dcityname": "天津", "acityname": "厦门", "date": "{}", "dcityid": 3, "token": "yourToken!"},
    {"dcity": "CGO", "acity": "XMN", "dcityname": "郑州", "acityname": "厦门", "date": "{}", "dcityid": 559, "token": "yourToken!"},
    {"dcity": "TNA", "acity": "XMN", "dcityname": "济南", "acityname": "厦门", "date": "{}", "dcityid": 144, "token": "yourToken!"},
    {"dcity": "SHE", "acity": "XMN", "dcityname": "沈阳", "acityname": "厦门", "date": "{}", "dcityid": 451,"token": "yourToken!"},
    {"dcity": "URC", "acity": "XMN", "dcityname": "乌鲁木齐", "acityname": "厦门", "date": "{}", "dcityid": 39,"token": "yourToken!"},
    {"dcity": "HRB", "acity": "XMN", "dcityname": "哈尔滨", "acityname": "厦门", "date": "{}", "dcityid": 5, "token": "yourToken!"},
    {"dcity": "HET", "acity": "XMN", "dcityname": "呼和浩特", "acityname": "厦门", "date": "{}", "dcityid": 103, "token": "yourToken!"}
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
