#-*-coding:utf-8-*-
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
import pymongo
import json

uas = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    ]

client = pymongo.MongoClient(DIANPING_URL,connect=False)
db=client[DIANPING_DB]

def save_to_mongo(result):
    if db[DIANPING_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False

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

def get_ip_kuai(page):
    headers = {
        'Referer': 'http://www.kuaidaili.com/free/intr/',
        'User-Agent': random.choice(USER_AGENTS)
    }
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
            full_ip = {"http":ip+":"+post}
            # print(full_ip)
            ip_list.append(full_ip)
        time.sleep(random.choice(range(1,3)))
    return ip_list

def get_ip_xila(page):
    headers3 = {
        'Referer': 'http://www.xicidaili.com/nt',
        'User-Agent': random.choice(USER_AGENTS)
    }
    ip_list=[]
    for page in range(1, page):
        print("-------获取第" + str(page) + "页ip--------")
        url = "http://www.xicidaili.com/nt/" + str(page)
        requset = requests.get(url=url, headers=headers3)  # ,proxies=json.loads(random.choice(ip_list))
        result_a = requset.text
        all_tr = BeautifulSoup(result_a, 'lxml').find_all('tr')[1:]
        for tr in all_tr:
            all_td = tr.find_all('td')
            ip = all_td[1].get_text()
            port = all_td[2].get_text()
            type = all_td[5].get_text().lower()
            full_ip = {type:(ip + ":" + port)}
            ip_list.append(full_ip)
        time.sleep(random.choice(range(2,4)))
    return ip_list

def crawl(url, ip_lsit):
    # socket.setdefaulttimeout(5)
    try:
        ip = random.choice(ip_lsit)
    except:
        return False
    else:
        proxies = ip
        headers2 = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                    'Cookie': '_lxsdk_cuid=1605e0182a1c8-0dcddc996964e2-5b452a1d-144000-1605e0182a1c8; _lxsdk=1605e0182a1c8-0dcddc996964e2-5b452a1d-144000-1605e0182a1c8; _hc.v=4fcafd03-8373-d150-6954-d7986b392b47.1513405645; s_ViewType=10; cy=2; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16064b2eea8-a3f-e63-0fe%7C%7C30',
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                    "Referer": "http://www.dianping.com/beijing/food",
                    "User-Agent": random.choice(uas),
                    }
    try:
        responese = requests.get(url, headers=headers2,proxies=proxies)
        html = responese.text
        soup = BeautifulSoup(html, "lxml")
        all_txt = soup.find_all("div", class_="txt")
        for txt in all_txt:
            try:
                title = txt.find("h4").get_text()
                shop_url = txt.find("div", class_="tit").find("a")["href"]
                star = txt.find("div", class_="comment").find("span")["class"][1][7:]
                if txt.find("a", class_="review-num"):
                    review_num = txt.find("a", class_="review-num").find("b").get_text()
                else:
                    review_num = ""
                if txt.find("a", class_="mean-price").find("b"):
                    mean_price = txt.find("a", class_="mean-price").find("b").get_text()[1:]
                else:
                    mean_price = ""
                food_type = txt.find_all("span", class_="tag")[0].get_text()
                location = txt.find_all("span", class_="tag")[1].get_text()
                address = txt.find("span", class_="addr").get_text()
                if star != "0":
                    taste = txt.find("span", class_='comment-list').find_all("b")[0].get_text()
                    environment = txt.find("span", class_='comment-list').find_all("b")[1].get_text()
                    service = txt.find("span", class_='comment-list').find_all("b")[2].get_text()
                else:
                    taste, environment, service = "", "", ""
                all = {
                    "标题": title,
                    "网址": shop_url,
                    "星级": star,
                    "评论人数": review_num,
                    "人均消费": mean_price,
                    "品类": food_type,
                    "区位": location,
                    "地址": address,
                    "口味": taste,
                    "环境": environment,
                    "服务": service,
                }
                save_to_mongo(all)
            except:
                pass

    except Exception:
        print(str(ip)+"不可用,剩余ip数："+str(len(ip_lsit)))
        if not ip_lsit:
            sys.exit()
        if ip in ip_lsit:
            ip_lsit.remove(ip)
        crawl(url, ip_lsit)
    else:
        print(str(ip) + "可用,剩余ip数：" + str(len(ip_lsit))+str(responese.status_code))
        if responese.status_code==200:
            with open("dz_ip.txt","a") as file:
                file.write(json.dumps(ip)+"\n")
                file.close()


def get_type_list(file):
    file = open(file,encoding="utf-8")
    type_list =[]
    for line in file:
        type_list.append(line.strip().split(":")[-1])
    return type_list

if __name__ == '__main__':
    headers = {
        'Referer': 'http://www.kuaidaili.com/free/intr/',
        'User-Agent': random.choice(USER_AGENTS)
    }
    IP_LIST =get_ip_xila(21)
    type_list = get_type_list("dianping_meishi.txt")
    for type in type_list[16:]:
        for page in range(1, 51):
            url = "http:" + type + "o2p" + str(page)
            t1 = threading.Thread(target=crawl, args=(url, IP_LIST))
            t1.start()
            time.sleep(random.choice(range(1, 3)))
    # for i in range(1,1000):
    #     t1 = threading.Thread(target=test_ip, args=(i, IP_LIST))
    #     t1.start()
    #     time.sleep(1)




