import json
import urllib.request
import urllib.parse

class GaoDE_coordinater(object):
    def __init__(self):
        pass

    def spider(self,content):
        headers = {
            'Referer': 'http://lbs.amap.com/console/show/picker',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        # print(content)
        keyword =urllib.parse.quote(
            content)
        url = "http://restapi.amap.com/v3/place/text?s=rsv3&children=&key=8325164e247e15eea68b59e89200988b&page=1&offset=10&city=120000&language=zh_cn&callback=jsonp_297203_&platform=JS&logversion=2.0&sdkversion=1.3&appname=http%3A%2F%2Flbs.amap.com%2Fconsole%2Fshow%2Fpicker&csid=ED97034C-EC17-4196-842E-0590BEBB2DA4&keywords="+ keyword
        requset = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(requset)
        result_a = response.read().decode('utf-8')
        # print(result_a)
        result_a = result_a.split("(", 1)[1][:-1]

        result_a = json.loads(result_a)

        if (result_a["info"]=="OK"):
            if result_a["pois"]:
                return result_a["pois"][0]["location"]
        else:
            return ""

if __name__ == '__main__':
    content = "北京风行在线技术有限公司"
    app = GaoDE_coordinater()
    a = app.spider(content)
    print(a)


