import re

import requests
import json
from bs4 import BeautifulSoup

headers = {
    'referer':'https://m.fang.com/bj.html',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

url = "https://m.fang.com/zf/?purpose=%D7%A1%D5%AC&jhtype=zf&city=%B1%B1%BE%A9&renttype=cz&c=zf&a=ajaxGetList&city=bj&r=0.41551867478289295&page=3"
response = requests.get(url,headers=headers)
html = response.content.decode("utf-8")
all_li = BeautifulSoup(html,'lxml').find_all("li")
for li in all_li:
    branch_url = "http:"+li.find("a",class_="tongjihref")["href"]
    title = li.find("h3").get_text().strip()
    all_p = li.find_all("p")
    rent_sale = li.find("span",class_="new").find("i").get_text()
    house_type = all_p[len(all_p)-3].get_text().split(" ")[1]
    # location = all_p[len(all_p)-2].find(re.compile("</span> (.*?) </p>",re.S))
    location =re.findall(re.compile("</span> (.*?) </p>",re.S),str(all_p[len(all_p)-2]))[0]
    # print(title,branch_url)
    tag = li.find("div",class_="stag")
    if tag:
        tags =re.findall(re.compile('<span class="red-z">(.*?)</span>',re.S),str(li))
        tag = ",".join(tags)
    else:
        tag = ""
    total ={
        "标题":title,
        "租金":rent_sale,
        "户型":house_type,
        "地址":location,
        "标签":tag,
        "网址":branch_url,
    }
    print(total)