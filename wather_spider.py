import requests
from bs4 import BeautifulSoup

## 爬去中国天气网，最低天气排名前10的城市
city_tem=[]
def parse_page(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    text = response.content.decode('utf8')
    soup = BeautifulSoup(text,'lxml')
    conMidtab = soup.find('div',{'class':'conMidtab'})
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            citys = {}
            tds = tr.find_all('td')
            if index == 0: #有的省名字在第二个td所以要作这个判断
                city_td = tds[1]
            else:
                city_td = tds[0]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            citys['city']=city
            citys['min_temp']=int(min_temp)
            city_tem.append(citys)

    return city_tem

if __name__ == '__main__':
    url = 'http://www.weather.com.cn/textFC/db.shtml'
    #url='http://www.weather.com.cn/textFC/hb.shtml'
    a = parse_page(url)
    a.sort(key=lambda b:b['min_temp'])

    print(a[0:9])



