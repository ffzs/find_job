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
    global my_ip_list
    headers = {
        'Referer': 'http://lbs.amap.com/console/show/picker',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    url = 'https://m.fang.com/zf/bj/JHAGT_390078672_594f9d02661d1a722b01c9a4b97c2d1f_164852129.html?listtype=0&listsub=0'
    try:
        response = requests.get(url, headers=headers,proxies=ip_dict)
        print(url,ip_dict,response)
        return True
    except Exception as e:
        print(ip_dict,e)
        return False

def main(num):
    global my_ip_list
    if make_sure(my_ip_list[num]):
        with open("ip_f.txt", "a", encoding='utf-8') as f:
            jsoninfo = json.dumps(my_ip_list[num])
            print(jsoninfo)
            f.write(jsoninfo + "\n")
            f.close()


if __name__ == '__main__':
    my_ip_list = get_ip_list("ip_fang.txt")
    print(my_ip_list)
    l = len(my_ip_list)
    for i in range(0,l):
        main(i)
    # groups = [x for x in range(0,l)]
    # pool = Pool()
    # pool.map(main, groups)




