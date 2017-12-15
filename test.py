import socket

import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    'Host':'m.zhaopin.com',
    'Referer': "https://m.zhaopin.com/beijing-530/?keyword=python&order=0&maprange=3&ishome=0",
    'Accept':"*/*",
    'User-Agent': "Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36",
    'Cookie':"urlfrom2=121127146; adfcid2=other; adfbid2=0; dywea=95841923.2181405878508596700.1513168384.1513243856.1513301404.4; dywez=95841923.1513301404.4.4.dywecsr=other|dyweccn=121113803|dywecmd=cnt|dywectr=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98; __utma=269921210.923620409.1513168386.1513243867.1513301407.4; __utmz=269921210.1513216118.2.2.utmcsr=other|utmccn=121113803|utmcmd=cnt|utmctr=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98; _ga=GA1.2.923620409.1513168386; _gid=GA1.2.894664418.1513168386; urlfrom=121127146; adfcid=other; adfbid=0; dyweb=95841923.9.10.1513301404; dywec=95841923; __utmb=269921210.8.10.1513301407; __utmc=269921210; _gat=1; __utmt=1"
}
socket.setdefaulttimeout(3)
url = "https://m.zhaopin.com/beijing-530/?keyword=python&order=0&maprange=3&ishome=0"
ip_dict = {"http": "http://221.233.85.54:3128"}
response = requests.get(url,headers = headers,proxies=ip_dict)
print(url,ip_dict,response)
print(response.text)