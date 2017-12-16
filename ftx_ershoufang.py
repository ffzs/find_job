#-*-coding:utf-8-*-
import requests
import random
import json
from bs4 import BeautifulSoup
from config import *
import re
from multiprocessing import Pool
import pymongo
from GaoDe_coordinate import GaoDE_coordinater

client = pymongo.MongoClient(FANG_URL,connect=False)
db=client[FANG_DB]



def get_ip_list(file):
    file = open(file)
    ip_list =[]
    for line in file:
        try:
            ip_list.append(json.loads(line.strip()))
        except:
            pass
    return ip_list

def save_to_mongo(result):
    if db[FANG_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False

def get_detials(branch_url):
    headers = {
        'Referer': 'https://m.fang.com/zf/bj/?jhtype=zf',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36'
    }
    # proxy = random.choice(self.ip_list)
    try:
        response = requests.get(branch_url,headers=headers)
        html = response.content.decode("gbk")
        soup = BeautifulSoup(html,"lxml")
        rent_type = soup.find("span",class_="f12 gray-8").get_text()[1:-1]
        all_li = soup.find("ul",class_="flextable").find_all("li")
        area = all_li[2].find("p").get_text()[:-2]
        floor = all_li[3].find("p").get_text()
        decoration = all_li[-1].find("p").get_text()
        all ={
            "交租方式":rent_type,
            "建筑面积":area,
            "楼层":floor,
            "装修":decoration,
        }
        return all
    except Exception as e:
        with open("fang_error.txt","a") as file:
            file.write(branch_url + "\n"+e+"\n")
            file.close()
        print(e)
        return {}


def get_total(url):
    # proxy = random.choice(self.ip_list)
    headers = {
        'Referer': 'https://m.fang.com/zf/bj/?jhtype=zf',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        html = response.content.decode("utf-8")
        all_li = BeautifulSoup(html, 'lxml').find_all("li")
        for li in all_li:
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
            detials = get_detials(branch_url)
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
            information = {**total,**detials}
            save_to_mongo(information)
    except Exception as e:
        with open("fang_error.txt","a") as file:
            file.write(url+"\n")
            file.close()
        print(e)
        pass

def main(page):
    print("--------正在爬第"+str(page)+"页-------------")
    url = "https://m.fang.com/zf/?purpose=%D7%A1%D5%AC&jhtype=zf&city=%B1%B1%BE%A9&renttype=cz&c=zf&a=ajaxGetList&city=bj&r=0.41551867478289295&page="+str(page)
    get_total(url)


if __name__ == '__main__':
    for i in range(362,1000):
        main(i)





