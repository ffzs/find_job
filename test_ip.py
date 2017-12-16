#-*-coding:utf-8-*-
import requests
import random
import json
from config import *
from multiprocessing import Pool

def get_ip_list(file):
    file = open(file)
    ip_list =[]
    for line in file:
        try:
            ip_list.append(json.loads(line.strip()))
        except:
            pass
    return ip_list

def make_sure(ip_dict):
    headers = {
        'Referer': 'https://m.fang.com/city/hotcity.jsp?city=bj',
        'User-Agent': random.choice(USER_AGENTS)
    }
    url = 'https://m.fang.com/zf/bj/'
    try:
        response = requests.get(url, headers=headers,proxies=ip_dict)
        print(url,ip_dict,response)
        return True
    except Exception as e:
        print(ip_dict,e)
        return False

def main(num):
    if make_sure(IP_LIST[num]):
        with open("ip_ftx.txt", "a", encoding='utf-8') as f:
            jsoninfo = json.dumps(IP_LIST[num])
            print(jsoninfo)
            f.write(jsoninfo + "\n")
            f.close()


if __name__ == '__main__':
    # MY_ip_list = get_ip_list("ip_.txt")
    # print(MY_ip_list)
    l = len(IP_LIST)
    groups = [x for x in range(0,l)]
    pool = Pool()
    pool.map(main, groups)




