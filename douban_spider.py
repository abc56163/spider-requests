import  requests
from bs4 import BeautifulSoup
import json
# 爬去豆瓣热门电影
class DouBanSpider:
    def __init__(self,url,headers):
        self.url = url
        self.headers =headers

    def get_page(self):
        response = requests.get(self.url, self.headers)
        text = response.text
        return text

    def parse_page(self,text):
        soup = BeautifulSoup(text,'lxml')
        list= soup.findAll('li',attrs={'data-category':'nowplaying'})
        return list


if __name__ == '__main__':
    movices=[]
    url = 'https://movie.douban.com/cinema/nowplaying/hefei/'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    page = DouBanSpider(url,headers)
    text = page.get_page()
    pares = page.parse_page(text)
    for li in pares:
        movice={}
        title = li['data-title']
        img = li.find('img')
        imgsrc = img['src']
        movice['title']=title
        movice['img_src']=imgsrc
        movices.append(movice)

    with open('movice.json','w') as fb:
        json.dump(movices,fb,ensure_ascii=False)


