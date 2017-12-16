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


class Fang_spider(object):
    def __init__(self):
        self.ip_list = self.get_ip_list("ip_tested.txt")
        self.headers = {
            'Referer': 'https://m.fang.com/city/hotcity.jsp?city=bj',
            'User-Agent': random.choice(USER_AGENTS)
        }
        pass


    def get_ip_list(self,file):
        file = open(file)
        ip_list =[]
        for line in file:
            try:
                ip_list.append(json.loads(line.strip()))
            except:
                pass
        return ip_list

    def save_to_mongo(self,result):
        if db[FANG_TABLE].insert(result):
            print('存储到MongoDB成功', result)
            return True
        return False

    def get_detials(self,branch_url):
        response = requests.get(branch_url,headers=self.headers)
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

    def get_total(self,url):
        a= 0
        proxy = random.choice(self.ip_list)
        try:
            response = requests.get(url, headers=self.headers,proxies=proxy)
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
                coordinate= GaoDE_coordinater.spider(a,location)
                tag = li.find("div", class_="stag")
                if tag:
                    tags = re.findall(re.compile('<span class="red-z">(.*?)</span>', re.S), str(li))
                    tag = ",".join(tags)
                else:
                    tag = ""
                detials = self.get_detials(branch_url)
                total = {
                    "标题": title,
                    "租金": rent_sale,
                    "户型": house_type,
                    "地址": location,
                    "坐标":coordinate,
                    "更新时间":refresh_time,
                    "标签": tag,
                    "网址": branch_url,
                }
                information = {**total,**detials}
                self.save_to_mongo(information)
        except:
            with open("fang_error.txt") as file:
                file.write(url+"\n"+proxy+"\n")
                file.close()
            pass

    def main(self,page):
        print("--------正在爬第"+str(page)+"页-------------")
        url = "https://m.fang.com/zf/?purpose=%D7%A1%D5%AC&jhtype=zf&city=%B1%B1%BE%A9&renttype=cz&c=zf&a=ajaxGetList&city=bj&r=0.41551867478289295&page="+str(page)
        self.get_total(url)


if __name__ == '__main__':
    app = Fang_spider()
    for i in range(1,600):
        app.main(i)





