import requests
import urllib
from lxml.html import fromstring


xpass = "//*[@id=\"route01\"]/div[5]/div[2]/div/ul/li[3]/ul/li/dl/dd"
cpass = "//*[@id=\"route01\"]/dl/dd[1]/ul/li[3]"
#//*[@id="route01"]/dl/dd[1]/ul/li[3]/span[2]

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

    # URL取得
    content = requests.get(f'https://transit.yahoo.co.jp/search/result?flatlon=&fromgid=&from={sta}&tlatlon=&togid=&to={end}&viacode=&via=&viacode=&via=&viacode=&via=&y=2019&m=07&d=22&hh=16&m2=4&m1=0&type=1&ticket=ic&expkind=1&ws=3&s=0&al=1&shin=1&ex=1&hb=1&lb=1&sr=1&kw={end}#route01').content

    # 駅の配列を作成
    sta_list = [station.text_content().replace("○", "") for station in fromstring(content).xpath(xpass)]
    sta_list.insert(0, from_station)
    sta_list.append(to_station)

    #値段を取得
    raw_price = fromstring(content).xpath(cpass)[0].text_content()
    price_str = raw_price.split("：")[-1].replace("円", "")
    price = int(price_str)

    return ResultData(sta_list, price)

if __name__ == "__main__":
    result = search("東京駅", "渋谷駅")
    print(result.cost, result.stations)
