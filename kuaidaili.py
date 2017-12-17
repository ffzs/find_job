# -*- coding: utf-8 -*-
import datetime
import re
import random
import threading
import time
import socket
import sys
from config import *
from YunDun import YunDun
import requests
from bs4 import BeautifulSoup

uas = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    ]

def get_cookie():
    global headers
    test_url ="http://www.kuaidaili.com/free/intr/"
    html = requests.get(test_url,headers=headers).text
    oo = re.findall('no="", oo = (.*?);qo = "qo=', html)[0]
    ri = ''.join(re.findall('setTimeout\(\"\D+\((\d+)\)\"', html))
    a = html.split(";",2)[-1]
    b = re.sub("0xff", "", a)
    s = re.findall("\d+", b)
    cookie = {'_ydclearance':YunDun.get_cookie(0,ri,oo,s)}
    return cookie

def get_ip(page):
    cookies = get_cookie()
    ip_list=[]
    for page in range(1,page):
        print("-------获取第"+str(page)+"页ip--------")
        url = "http://www.kuaidaili.com/free/intr/"+str(page)+"/"
        response = requests.get(url,headers=headers,cookies=cookies).text
        # print(response)
        soup = BeautifulSoup(response,'lxml')
        all_tr = soup.find_all("tr")
        for tr in all_tr[1:]:
            ip = tr.find_all("td")[0].get_text()
            post = tr.find_all("td")[1].get_text()
            full_ip = ip+":"+post
            # print(full_ip)
            ip_list.append(full_ip)
        time.sleep(random.choice(range(1,3)))
    return ip_list

def test_ip(code, ip_lsit):
    socket.setdefaulttimeout(5)
    try:
        ip = random.choice(ip_lsit)
    except:
        return False
    else:
        proxies = {
            "http": ip,
        }
        headers2 = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                    "Referer": "http://www.dianping.com/beijing/food",
                    "User-Agent": random.choice(uas),
                    }
    try:
        hz_url = "http://www.dianping.com/beijing/food"
        hz_r = requests.get(hz_url, headers=headers2, proxies=proxies)
        if hz_r.status_code != "200":
            False
    except Exception as e:
        print(e)
        if not ip_lsit:
            sys.exit()
        # 删除不可用的代理IP
        if ip in ip_lsit:
            ip_lsit.remove(ip)
        # 重新请求URL
        test_ip(code, ip_lsit)
    else:
        with open("dz_ip.txt","a") as file:
            file.write(ip+"\n")
            file.close()
        if ip in ip_lsit:
            ip_lsit.remove(ip)
        date = datetime.datetime.now().strftime('%H:%M:%S')
        print ("第%s次测试%s 状态[%s] 测试时间 [%s]： (剩余可用代理IP数：%s)" % (code, hz_r,date, ip, len(ip_lsit)))

if __name__ == '__main__':
    headers = {
        'Referer': 'http://www.kuaidaili.com/free/intr/',
        'User-Agent': random.choice(USER_AGENTS)
    }
    IP_LIST =get_ip(40)
    for i in range(1,1000):
        t1 = threading.Thread(target=test_ip, args=(i, IP_LIST))
        t1.start()
        time.sleep(1)




