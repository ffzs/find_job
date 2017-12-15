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

    def make_sure(self,ip_dict):
        socket.setdefaulttimeout(3)
        url = 'https://www.baidu.com/'
        try:
            response = requests.get(url, proxies=ip_dict)
            print(url,ip_dict,response)
            return True
        except Exception as e:
            print(ip_dict,e)
            return False



    def spider(self,page):
        headers = {
                'Referer': 'http://www.xicidaili.com/nn/',
                'User-Agent': '"Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36"'
                    }
        # list =[]
        url = "http://www.xicidaili.com/nn/" + str(page)
        requset = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(requset)
        result_a = response.read().decode('utf-8')
        all_tr = BeautifulSoup(result_a,'lxml').find_all('tr')[1:]
        for tr in all_tr:
            all_td = tr.find_all('td')
            ip = all_td[1].get_text()
            port = all_td[2].get_text()
            type = all_td[5].get_text().lower()
            ip_dict = {type:type+"://"+ip+":"+port}
            if self.make_sure(ip_dict):
                with open("ip_pool.txt","a",encoding='utf-8') as f:
                    jsoninfo = json.dumps(ip_dict)
                    print(jsoninfo)
                    f.write(jsoninfo+"\n")
                    f.close()

if __name__ == '__main__':
    app = DailiIP()
    groups = [x for x in range(1, 100)]
    pool = Pool()
    pool.map(app.spider, groups)


