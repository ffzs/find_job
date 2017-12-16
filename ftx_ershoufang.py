#-*-coding:utf-8-*-
import requests
import random
import json
from bs4 import BeautifulSoup
from config import *
import re
from multiprocessing import Pool
import pymongo

client = pymongo.MongoClient(FANG_URL,connect=False)
db=client[FANG_DB]

headers = {
    'Referer': 'https://m.fang.com/city/hotcity.jsp?city=bj',
    'User-Agent': random.choice(USER_AGENTS)
}
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

def get_total(url):
    headers = {
        'Referer': 'https://m.fang.com/bj.html',
        'User-Agent': random.choice(USER_AGENTS)
    }
    ip_list = get_ip_list("ip_tested.txt")
    proxy = random.choice(ip_list)
    try:
        response = requests.get(url, headers=headers,proxies=proxy)
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
                "更新时间":refresh_time,
                "标签": tag,
                "网址": branch_url,
            }
            save_to_mongo(total)
    except:
        with open("fang_error.txt") as file:
            file.write(url+"\n"+proxy+"\n")
            file.close()
        pass

def main(page):
    print("--------正在爬第"+str(page)+"页-------------")
    url = "https://m.fang.com/zf/?purpose=%D7%A1%D5%AC&jhtype=zf&city=%B1%B1%BE%A9&renttype=cz&c=zf&a=ajaxGetList&city=bj&r=0.41551867478289295&page="+str(page)
    get_total(url)


if __name__ == '__main__':
    for i in range(1,600):
        main(i)





