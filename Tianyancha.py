import urllib.parse
import urllib.request
from lxml import etree

class Tianyancha(object):

    def __init__(self):
        pass

    def crawl(self,content):
        headers = {
                    'Referer': 'https://m.tianyancha.com/?jsid=SEM-BAIDU-PZPC-000000',
                    'User-Agent': '"Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36"'
                }

        keyword =urllib.parse.quote(content)
        # url = "https://www.tianyancha.com/search?key="+keyword+"&checkFrom=searchBox"
        url = "https://m.tianyancha.com/search?key="+keyword+"&checkFrom=searchBox"
        requset = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(requset)
        result_a = response.read().decode('utf-8')
        selector = etree.HTML(result_a)
        com_name = selector.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/a/span/em/text()')
        if com_name:
            tiany_url = "https://m.tianyancha.com"+selector.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/a/@href')[0]
            capital = selector.xpath('/html/body/div[2]/div[4]/div[1]/div[4]/div/div/div[2]/span/text()')[0]
            register_time = selector.xpath('/html/body/div[2]/div[4]/div[1]/div[4]/div/div/div[3]/span/text()')[0]
            # telephone = selector.xpath('//*[@id="web-content"]/div/div/div/div[1]/div[3]/div[1]/div[2]/div[2]/div[2]/div/span[2]/text()')[0]
            score = selector.xpath('/html/body/div[2]/div[4]/div[1]/div[4]/div/svg/text[1]/text()')[0]
            all = {
                "公司":com_name[0],
                "注册资金":capital,
                "注册时间":register_time,
                # "电话":telephone,
                "得分":score,
                "详情地址":tiany_url,
            }
            return all

if __name__ == '__main__':
    content = "北京布雷恩科技有限公司"
    app = Tianyancha()
    a = app.crawl(content)
    print(a)