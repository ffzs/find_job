#encoding:utf-8
import pymongo
import random
import json
import re
from multiprocessing import Pool
import requests
import time
from bs4 import BeautifulSoup
from lxml import etree
from config import *
from GaoDe_coordinate import GaoDE_coordinater
from Tianyancha import Tianyancha

client = pymongo.MongoClient(MONGO_URL,connect=False)
db=client[MONGO_DB]

headers = {
    'Referer': 'https://m.zhaopin.com/beijing-530/?keyword=python&order=0&maprange=3&ishome=0',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36',
}

def get_ip_list(file):
    file = open(file)
    ip_list = []
    for line in file:
        ip_list.append(line.strip())

    return ip_list

def get_average(job_sal):
    cut = job_sal.split("-")
    s = 0
    if len(cut)==2:
        for item in cut:
            if "万" in item:
                p = item[:-1]
                q = int(float(p) * 10000)
                # print(p,q)
            else:
                p = item[:-1]
                q = int(float(p) * 1000)
            s += q
    return int(s/len(cut))


def get_job_details(job_url):
    headers = {
        'Referer': 'https://m.zhaopin.com/beijing-530/?keyword=python&order=0&maprange=3&ishome=0',
        'User-Agent': random.choice(USER_AGENTS),
    }
    a, b = " ", ","
    about_job, tags = [], []
    ip_list= get_ip_list("ip_pool.txt")
    proxy = json.loads(random.choice(ip_list))
    print(proxy)
    request = requests.get(job_url, headers=headers,proxies=proxy)
    selector = etree.HTML(request.text)
    # print(job_url)
    job_name = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/h1/text()')
    if job_name:
        job_sal = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/div[1]/text()')[0]
        average_sal = get_average(job_sal)
        company_name = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[2]/text()')[0]
        company_address = selector.xpath('//*[@id="r_content"]/div[1]/div/div[2]/div/text()')
        if company_address:
            pass
        else:
            company_address =[""]
        coordinate = GaoDE_coordinater.spider(a, company_address[0])
        job_code = job_url.split("/")[-2]
        about_main = BeautifulSoup(request.text, 'lxml').find_all('div', class_="about-main")
        if about_main:
            pass
        else:
            about_main = BeautifulSoup(request.text, 'lxml').find_all('div', class_="about-main")
        for p in about_main:
            about_job.append(p.get_text().strip())
        about_job = a.join(about_job)
        # if KEYWORD in (str(about_job)+str(job_name[0])):
        all_tag = BeautifulSoup(request.text, 'lxml').find_all('span', class_="tag")
        tag_number = len(all_tag)
        for tag in all_tag:
            tags.append(tag.get_text())
        tag = b.join(tags)
        company_condition = Tianyancha.crawl(a,company_name)
        total = {
            "工作编号":job_code,
            "工作名称": job_name[0],
            "工资范围": job_sal,
            "参考平均工资":average_sal,
            "公司名称": company_name,
            "公司地址": company_address[0],
            "位置坐标":coordinate,
            "工作详情": about_job,
            "工作标签": tag,
            "工作标签数":tag_number,
            "智联网址":job_url,
        }
        print(total,company_condition)
        if company_condition:
            return {**total,**company_condition}
        else:
            return total
    else:
        return ""

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        # print('存储到MongoDB成功', result)
        return True
    return False

def get_job_url(url):
    request = requests.get(url,headers=headers)
    # print(request.text)
    all_a = BeautifulSoup(request.text,'lxml').find_all('a',class_="boxsizing")
    for a in all_a:
        job_url = 'https://m.zhaopin.com'+a["data-link"]
        result = get_job_details(job_url)
        time.sleep(random.choice(range(1,3)))
        if result:
            save_to_mongo(result)

def main(page):
    print("--------------正在爬第"+str(page)+"页-----------------")
    A_url = 'https://m.zhaopin.com/'+CITY+'/?keyword='+KEYWORD+'&pageindex='+str(page)+'&maprange=3&publishdate=30&islocation=0'
    get_job_url(A_url)

if __name__ == '__main__':
    for i in range(1,316):
        # if (i%10)==0:
        #     time.sleep(240)
        # else:
        #     pass
        main(i)

    # groups = [x for x in range(34, 100)]
    # pool = Pool()
    # pool.map(main, groups)
