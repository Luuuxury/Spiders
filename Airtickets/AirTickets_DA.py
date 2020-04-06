import pandas as pd
import matplotlib.pyplot as plt

csv_data = pd.read_csv('TO_XMN2020-03-21 00:00:00.csv')
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)

price = csv_data.get("机票价格")
departure_time = csv_data.get("出发时间")  # Series
# 过滤时间，把日期 和 小时分钟分开
departure_time_h = departure_time.str.split(' ', expand=True).rename(columns={0: '日期', 1: '时间'})  # DataFrame
time_price = pd.concat([departure_time_h['时间'], price], axis=1)
# print(time_price.info())
# print(time_price.tail(50))

sum_list = []
for h in range(6, 23):
    # 分别对 6-7 7-8 .... 22-23 时段的机票价格求均值
    time_price_h_h = time_price[(pd.to_datetime(time_price['时间'], format='%H:%M:%S') >= pd.to_datetime('{}:00:00'.format(h), format='%H:%M:%S')) &
                                (pd.to_datetime(time_price['时间'], format='%H:%M:%S') <= pd.to_datetime('{}:00:00'.format(h+1), format='%H:%M:%S'))]  # DataFrame
    average_price = time_price_h_h['机票价格'].sum() / len(time_price_h_h)
    sum_list.append(average_price)

print(sum_list)
h_h = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
plt.plot(h_h, sum_list)
plt.show()





