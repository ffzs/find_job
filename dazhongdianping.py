#-*-coding:utf-8-*-
import json
import random
import pymongo
import requests
import time
from bs4 import BeautifulSoup
from config import *

client = pymongo.MongoClient(DIANPING_URL,connect=False)
db=client[DIANPING_DB]

def save_to_mongo(result):
    if db[DIANPING_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False

def get_ip_list(file):
    file = open(file)
    ip_list =[]
    for line in file:
        try:
            ip_list.append(json.loads(line.strip()))
        except:
            pass
    return ip_list

def get_type_list(file):
    file = open(file,encoding="utf-8")
    type_list =[]
    for line in file:
        type_list.append(line.strip().split(":")[-1])
    return type_list

def crwal(url):
    headers = {
        'Cookie': '_lxsdk_cuid=1605e56c7b779-0dd789ebd32644-b7a103e-100200-1605e56c7b9c8; _lxsdk=1605e56c7b779-0dd789ebd32644-b7a103e-100200-1605e56c7b9c8; _hc.v=12ed2395-1f5f-af9f-a3f2-cabf60795723.1513411234; s_ViewType=10; cy=2; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=1605fa02fa9-49d-7c0-d3f%7C%7C21',
        'User-Agent': random.choice(USER_AGENTS),
        'Referer': 'http://www.dianping.com/beijing/food'
    }
    ip_list = get_ip_list("ip_DZDP.txt")
    proxy = random.choice(ip_list)
    print(headers,proxy)
    responese = requests.get(url,headers=headers)
    html = responese.text
    soup = BeautifulSoup(html,"lxml")
    all_txt = soup.find_all("div",class_="txt")
    for txt in all_txt:
        try:
            title = txt.find("h4").get_text()
            shop_url = txt.find("div",class_="tit").find("a")["href"]
            star = txt.find("div",class_="comment").find("span")["class"][1][7:]
            if txt.find("a", class_="review-num"):
                review_num = txt.find("a", class_="review-num").find("b").get_text()
            else:
                review_num = ""
            if txt.find("a",class_="mean-price").find("b"):
                mean_price = txt.find("a",class_="mean-price").find("b").get_text()[1:]
            else:
                mean_price = ""
            food_type = txt.find_all("span",class_="tag")[0].get_text()
            location = txt.find_all("span",class_="tag")[1].get_text()
            address = txt.find("span",class_="addr").get_text()
            if star!="0":
                taste = txt.find("span",class_='comment-list').find_all("b")[0].get_text()
                environment = txt.find("span",class_='comment-list').find_all("b")[1].get_text()
                service = txt.find("span",class_='comment-list').find_all("b")[2].get_text()
            else:
                taste,environment,service ="","",""
            all = {
                "标题":title,
                "网址":shop_url,
                "星级":star,
                "评论人数":review_num,
                "人均消费":mean_price,
                "品类":food_type,
                "区位":location,
                "地址":address,
                "口味":taste,
                "环境":environment,
                "服务":service,
            }
            save_to_mongo(all)
        except:
            pass

if __name__ == '__main__':
    type_list = get_type_list("dianping_meishi.txt")
    for type in type_list[16:]:
        for page in range(1,51):
            url = "http:"+type+"o2p"+str(page)
            time.sleep(random.choice(range(1, 3)))
            print(url)
            crwal(url)


