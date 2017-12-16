#-*-coding:utf-8-*-
import requests
import random
import json


headers = {
        'Referer': 'http://lbs.amap.com/console/show/picker',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }

def get_ip_list(file):
    file = open(file)
    ip_list =[]
    for line in file:
        ip_list.append(line.strip())
    return ip_list

if __name__ == '__main__':
    ip_list = get_ip_list("ip_.txt")
    url ="https://m.fang.com/zf/?purpose=%D7%A1%D5%AC&jhtype=zf&city=%B1%B1%BE%A9&renttype=cz&c=zf&a=ajaxGetList&city=bj&r=0.8237764370327307&page=4"
    response = requests.get(url=url,headers= headers,proxies = json.loads(random.choice(ip_list))).content.decode("utf-8")
    print(response)

