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


headers = {
    'Cookie':'_lxsdk_cuid=1605e0182a1c8-0dcddc996964e2-5b452a1d-144000-1605e0182a1c8; _lxsdk=1605e0182a1c8-0dcddc996964e2-5b452a1d-144000-1605e0182a1c8; _hc.v=4fcafd03-8373-d150-6954-d7986b392b47.1513405645; s_ViewType=10; cy=2; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16064b2eea8-a3f-e63-0fe%7C%7C30',
    'Referer':'http://www.dianping.com/beijing/life',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko'
}

url = "http://www.dianping.com/tianjin/food"
req =requests.get(url,headers=headers)
print(req.text)

