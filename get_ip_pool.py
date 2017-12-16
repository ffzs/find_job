import random
import socket
import urllib.request
import urllib.parse
import json
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup


class DailiIP(object):
    def __init__(self):
        pass

    def get_ip_list(self,file):
        file = open(file)
        ip_list = []
        for line in file:
            ip_list.append(line.strip())
        return ip_list

    def make_sure(self,ip_dict):
        socket.setdefaulttimeout(3)
        url = 'http://www.fang.com/?s=BDPZ-BL'
        try:
            response = requests.get(url, proxies=ip_dict)
            print(url,ip_dict,response)
            return True
        except Exception as e:
            print(ip_dict,e)
            return False

    def spider(self,page):
        headers = {
                'Referer': 'http://www.xicidaili.com/wt/',
                'User-Agent': '"Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36"'
                    }
        # list =[]
        url = "http://www.xicidaili.com/wt/" + str(page)
        # ip_list = self.get_ip_list("ip_.txt")
        # print(ip_list)
        requset = requests.get(url=url, headers=headers)  #,proxies=json.loads(random.choice(ip_list))
        result_a = requset.text
        all_tr = BeautifulSoup(result_a,'lxml').find_all('tr')[1:]
        for tr in all_tr:
            all_td = tr.find_all('td')
            ip = all_td[1].get_text()
            port = all_td[2].get_text()
            type = all_td[5].get_text().lower()
            ip_dict = {type:type+"://"+ip+":"+port}
            if self.make_sure(ip_dict):
                with open("ip_fang.txt","a",encoding='utf-8') as f:
                    jsoninfo = json.dumps(ip_dict)
                    # print(jsoninfo)
                    f.write(jsoninfo+"\n")
                    f.close()

if __name__ == '__main__':
    app = DailiIP()
    for i in range(2,20):
        app.spider(i)
    # groups = [x for x in range(1,10)]
    # pool = Pool()
    # pool.map(app.spider, groups)


