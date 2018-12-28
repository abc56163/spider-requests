import requests
from lxml import etree
from bs4 import BeautifulSoup
import re

course=[]

def vmware_get(url):
    headers={
        'headers': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        "Cookie": "pgv_pvi=9491871479; uchome_2132_smile=1D1; uchome_2132_nofavfid=1; uchome_2132_saltkey=eaoO8I06; uchome_2132_lastvisit=1545723538; uchome_2132_sid=w2UfYb; uchome_2132_Hey_jsTips_0_86400=1; pgv_info=ssid=s288439950; ts_last=bbs.vmanager.cn/forum-189-1.html; pgv_pvid=7188177906; ts_uid=5428402610; pgv_si=s2123296768; uchome_2132_ulastactivity=52ff3NqHI9xtqowZ211AhBJgvwDmp%2B9qLI10breKryOWtB2Ww1Pz; uchome_2132_auth=4a29OyM2LUoedASK3UThM4wCnBQqDDTKwN8M%2F%2BE0HBRodBnq4wwY6AfCXdwKQEDh1Y5sw70GSaXN%2BRIs4cVaNP1eQQ; uchome_2132_lastcheckfeed=54287%7C1545727159; uchome_2132_visitedfid=189; uchome_2132_Hey_jsTips_54287_86400=1; uchome_2132_lastact=1545727244%09forum.php%09forumdisplay; uchome_2132_st_t=54287%7C1545727244%7Cdc67b5ef9bb11d676e4098c6d0d47160; uchome_2132_forum_lastvisit=D_189_1545727244"
    }
    response = requests.get(url,headers=headers)
    text = response.content.decode('gbk')
    page=etree.HTML(text)
    #urls = page.xpath('//table[@id="threadlisttableid"]//tbody[position()>8]/tr/th/a[@class="s xst"]//@href')
    urls = page.xpath('//table[@id="threadlisttableid"]//tbody/tr/th/a[@class="s xst"]//@href')
    for url in urls:
        massage = {}
        response = requests.get(url,headers=headers)
        text = response.content.decode('gbk')
        page = etree.HTML(text)
        # print(etree.tostring(page).decode('gbk'))
        names = page.xpath('//*[@id="thread_subject"]/text()')
        links = page.xpath('//td[@class="t_f"]//script[position()<2]/text()')
        if links == []:
            pass
        else:
            link = re.findall('http://[^\s]*.swf|http://[^\s]*mp4', links[0])
            massage['name'] = names
            massage['link'] = link
            course.append(massage)
    return course


def get_mp4(url): # 下载视频
    video = vmware_get(url)
    for v in video:
        name = v['name'][0]
        links = v['link'][0]
        if '.mp4' in links:
            link = links
        else:
            link = links.replace('/e/1', '/e/6')
            # link = link2.replace('.swf', '.mp4')
        repnose = requests.get(link)
        mp4 = repnose.content
        name = name + '.mp4'
        with open('/root/Desktop/vsphere/' + name, 'wb') as s:
            s.write(mp4)


def get_link(url):
    video = vmware_get(url)
    for v in video:
        name = v['name'][0]
        links = v['link'][0]
        if '.mp4' in links:
            link = links
        else:
            link2 = links.replace('/e/1', '/e/6')
            link = links.replace('.swf', '.mp4')
        #urls = name+ ":" +link
        urls = ':'.join([name,link])
        with open('/root/Desktop/links.txt','a+') as f:
            f.write(urls+'\n')



#url = ['http://bbs.vmanager.cn/forum-189-1.html']
#url = ['http://bbs.vmanager.cn/forum-201-1.html','http://bbs.vmanager.cn/forum-201-2.html']
#url = ['http://bbs.vmanager.cn/forum-187-1.html']
#url = ['http://bbs.vmanager.cn/forum-183-1.html']
url = ['http://bbs.vmanager.cn/forum-213-1.html']

#get_mp4(url)
for i in url:
    get_link(i)
