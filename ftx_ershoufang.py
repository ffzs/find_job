#-*-coding:utf-8-*-
import threading
import requests
import random
import json
import time
import sys
from bs4 import BeautifulSoup
from config import *
import re
import pymongo
import socket
from GaoDe_coordinate import GaoDE_coordinater

client = pymongo.MongoClient(FANG_URL,connect=False)
db=client[FANG_DB]


def save_to_mongo(result):
    if db[FANG_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False

def get_detials(total,ip_list):
    global lock
    headers = {
        'Referer': 'https://m.fang.com/zf/bj/?jhtype=zf',
        'User-Agent': random.choice(USER_AGENTS)
    }
    try:
        ip = random.choice(ip_list)
    except:
        return False
    else:
        proxies = ip
    try:
        response = requests.get(total["网址"],headers=headers,proxies=proxies)
        html = response.content.decode("gbk")
        soup = BeautifulSoup(html,"lxml")
        rent_type = soup.find("span",class_="f12 gray-8").get_text()[1:-1]
        all_li = soup.find("ul",class_="flextable").find_all("li")
        area = all_li[2].find("p").get_text()[:-2]
        floor = all_li[3].find("p").get_text()
        decoration = all_li[-1].find("p").get_text()
        detials ={
            "交租方式":rent_type,
            "建筑面积":area,
            "楼层":floor,
            "装修":decoration,
        }
        information = {**total, **detials}
        if lock.acquire():
            save_to_mongo(information)
            lock.release()
    except Exception as e:
        print(e)
        print(str(ip) + "不可用,剩余ip数：" + str(len(ip_list)))
        if not ip_list:
            sys.exit()
        if ip in ip_list:
            ip_list.remove(ip)
        get_detials(total, ip_list)
    else:
        print(str(ip) + "可用###剩余ip数：" + str(len(ip_list)) + "###网络状态："+str(response.status_code))
        if response.status_code == 200:
            with open("ftx_ip.txt", "a") as file:
                file.write(json.dumps(ip) + "\n")
                file.close()

def get_total(url,ip_list):
    socket.setdefaulttimeout(5)
    try:
        ip = random.choice(ip_list)
    except:
        return False
    else:
        proxies = ip
    headers = {
        'Referer': 'https://m.fang.com/zf/bj/?jhtype=zf',
        'User-Agent': random.choice(USER_AGENTS)
    }
    try:
        response = requests.get(url, headers=headers,proxies=proxies)
        html = response.content.decode("utf-8")
        all_li = BeautifulSoup(html, 'lxml').find_all("li")
        for li in all_li:
            try:
                branch_url = "http:" + li.find("a", class_="tongjihref")["href"]
                title = li.find("h3").get_text().strip()
                all_p = li.find_all("p")
                rent_sale = li.find("span", class_="new").find("i").get_text()
                house_type = all_p[len(all_p) - 3].get_text().split(" ")[1]
                refresh_time = li.find("span",class_="flor").get_text()
                location = re.findall(re.compile("</span> (.*?) </p>", re.S), str(all_p[len(all_p) - 2]))[0]
                # print(title,branch_url)
                # coordinate= GaoDE_coordinater.spider(a,location)
                tag = li.find("div", class_="stag")
                if tag:
                    tags = re.findall(re.compile('<span class="red-z">(.*?)</span>', re.S), str(li))
                    tag = ",".join(tags)
                else:
                    tag = ""
                total = {
                    "标题": title,
                    "租金": rent_sale,
                    "户型": house_type,
                    "地址": location,
                    # "坐标":coordinate,
                    "更新时间":refresh_time,
                    "标签": tag,
                    "网址": branch_url,
                }
                t1 = threading.Thread(target=get_detials, args=(total, ip_list))
                t1.start()
                time.sleep(0.3)
            except Exception as e:
                print(e)
    except Exception:
        print(str(ip) + "不可用,剩余ip数：" + str(len(ip_list)))
        if not ip_list:
            sys.exit()
        if ip in ip_list:
            ip_list.remove(ip)
        get_total(url, ip_list)
    else:
        print(str(ip) + "可用###剩余ip数：" + str(len(ip_list)) + "###网络状态："+str(response.status_code))
        if response.status_code == 200:
            with open("ftx_.txt", "a") as file:
                file.write(json.dumps(ip) + "\n")
                file.close()

def get_ip_xila(page):
    headers3 = {
        'Referer': 'http://www.xicidaili.com/nn',
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

def get_ip_text(file):
    file = open(file)
    ip_list =[]
    for line in file:
        try:
            ip_list.append(json.loads(line.strip()))
        except:
            pass
    return ip_list

if __name__ == '__main__':
    # IP_LIST = get_ip_xila(21)
    IP_LIST = get_ip_text("ftx_ip.txt")
    lock =threading.Lock()
    print(IP_LIST)
    for page in range(7239,8000):
        print("---------爬取第"+str(page)+"页------------")
        url = "https://m.fang.com/zf/?purpose=%D7%A1%D5%AC&jhtype=zf&city=%B1%B1%BE%A9&renttype=cz&c=zf&a=ajaxGetList&city=bj&r=0.41551867478289295&page=" + str(
            page)
        get_total(url, IP_LIST)








