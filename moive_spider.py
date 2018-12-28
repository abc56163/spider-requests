import requests
from lxml import etree

def paser_page(url):
    movie_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    # requests 自己会猜测编码，如果猜错了就会出现乱码，
    # 例如页面是gbk的，那么就需要利用content转换而二进制，然后在decode下
    #text = response.content.decode(‘gbk’)
    text = response.text
    #解析html
    movie = etree.HTML(text)
    movie_link=movie.xpath("//div[@id='content']//div[@class='post clearfix']//a[@class='entry-thumb lazyload']//@href")
    for url in movie_link:
        movie_detail = {}
        text = requests.get(url,headers=headers).text
        movie = etree.HTML(text)
        movie_name = movie.xpath("//div[@class='entry lazyload']//div[2]/h3[2]/text()")
        movie_link = movie.xpath("//div[@class='entry lazyload']//div[@id='zdownload']//a//@href")
        movie_detail['movie_name']=movie_name
        movie_detail['movie_link']=movie_link
        movie_list.append(movie_detail)
    return movie_list


url = 'https://www.btdx8.com/newmovie'

movie = paser_page(url)
print(movie)

