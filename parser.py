import requests
import urllib
import datetime
import re
from lxml.html import fromstring

# 各Xpath
cpass = "//*[@id=\"route01\"]/dl/dd[1]/ul/li[3]"
tpass = "//*[@id=\"route01\"]/div[5]/div[2]/div/ul/li[3]/ul/li/dl/dt"

class ResultData:
    stations:[str]
    cost:int

    def __init__(self, stations:[str], cost:int):
        self.stations = stations
        self.cost = cost

def search(from_station:str, to_station:str) -> ResultData:

    #URL encode
    sta = urllib.parse.quote(from_station)
    end = urllib.parse.quote(to_station)

    #現在時刻取得
    now = datetime.datetime.now()

    # URL取得
    content = requests.get(f'https://transit.yahoo.co.jp/search/result?flatlon=&fromgid=&from={sta}&tlatlon=&togid=&to={end}&viacode=&via=&viacode=&via=&viacode=&via=&y={now.year}&m={str(now.month).zfill(2)}&d={str(now.day).zfill(2)}&hh={str(now.hour).zfill(2)}&m2={str(now.minute)[1:]}&m1={str(now.minute).zfill(2)[:1]}&type=1&ticket=ic&expkind=1&ws=3&s=0&shin=1&lb=1&kw={end}#route01').content

    # 駅の配列を生成
    sta_list = []
    list_len = [sta1.text_content() for sta1 in fromstring(content).xpath("//*[@id=\"route01\"]/div[5]/div[2]/div")]
    for i in range(len(list_len)+1):
        if i % 2 == 0:
            sta_list += [station.text_content().replace("○", "") for station in fromstring(content).xpath(f"//*[@id=\"route01\"]/div[5]/div[2]/div[{i}]/dl/dt/a")]
        else:
            sta_list += [station.text_content().replace("○", "") for station in fromstring(content).xpath(f"//*[@id=\"route01\"]/div[5]/div[2]/div[{i}]/ul/li[3]/ul/li/dl/dd")]
            sta_list += [station.text_content().replace("○", "") for station in fromstring(content).xpath(f"//*[@id=\"route01\"]/div[5]/div[2]/div[{i}]/div/ul/li[3]/ul/li/dl/dd")]
            sta_list += [station.text_content().replace("○", "") for station in fromstring(content).xpath(f"//*[@id=\"route01\"]/div[5]/div[2]/div[{i}]/ul/li[2]/ul/li/dl/dd")]

    # 出発駅と到着駅を配列に追加
    sta_list.insert(0, from_station)
    sta_list.append(to_station)

    # 値段を取得（正規表現ver.）
    raw_price = fromstring(content).xpath(cpass)[0].text_content()
    price_str = raw_price.split("：")[-1].replace(",", "")
    price = (re.search('^\d+' , price_str)).group(0)

    return ResultData(sta_list, price)

# 確認出力
# result = search("東京", "渋谷")
# print(result.stations)
# print(result.cost)
