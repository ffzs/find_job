#-*-coding:utf-8-*-
import re
import requests
import json
from bs4 import BeautifulSoup

headers = {
    'referer':'https://m.fang.com/bj.html',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

url = "https://m.fang.com/zf/bj/JHAGT_390119029_81f1ea043b1d7c26706aad691e97ce20_164207206.html"
response = requests.get(url,headers=headers)
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
print(all)
