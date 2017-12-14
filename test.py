import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
}

url = "https://m.zhaopin.com/jobs/000101241000007/"
a ,b= "\n",","
about_job,tags= [],[]
request = requests.get(url,headers=headers).text
selector=etree.HTML(request)
job_name =selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/h1/text()')
job_sal = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/div[1]/text()')
company_name = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[2]/text()')
company_address = selector.xpath('//*[@id="r_content"]/div[1]/div/div[2]/div/text()')
about_main = BeautifulSoup(request,'lxml').find('div',class_="about-main").find_all('p')
for p in about_main:
    about_job.append(p.get_text())
about_job=a.join(about_job)
all_tag = BeautifulSoup(request,'lxml').find_all('span',class_="tag")
for tag in all_tag:
    tags.append(tag.get_text())
tag = b.join(tags)
total = {
    "工作名称":job_name,
    "工资范围":job_sal,
    "公司名称":company_name,
    "公司地址":company_address,
    "工作详情":about_job,
    "工作标签":tag,
}
print(total)
