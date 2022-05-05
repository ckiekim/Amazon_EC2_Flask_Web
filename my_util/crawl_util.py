import requests, time
from urllib.parse import quote
from selenium import webdriver
from bs4 import BeautifulSoup
from flask import current_app
import pandas as pd

def siksin(place):
    url_base = 'https://www.siksinhot.com'
    url_sub = '/search?keywords=' + quote(place)
    url = url_base + url_sub
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    lis = soup.select_one('.listTy1').find('ul').find_all('li')

    rest_list = []
    for i in range(0, len(lis), 5):
        store = lis[i].select_one('.store').string
        img = lis[i].find('img').attrs['src'].split('?')[0]
        href = lis[i].find('a').attrs['href']
        url = url_base + href
        req = requests.get(url) 
        rest = BeautifulSoup(req.text, 'html.parser')
        feature = rest.select_one('.store_name_score').find('p').string
        tel = rest.select_one('.p_tel').find('p').get_text()
        addr = rest.select_one('.txt_adr').get_text()
        rest_list.append({'store':store, 'img':img, 'feature':feature,
                          'tel':tel, 'addr':addr, 'href':url})
    return rest_list

def genie():
    url = 'https://www.genie.co.kr/chart/top200'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get(url, headers = header)
    soup = BeautifulSoup(req.text, 'html.parser')
    trs = soup.select_one('.list-wrap').find('tbody').select('tr.list')

    music_list = []
    for index, tr in enumerate(trs):
        num = tr.select_one('.number').get_text()
        rank = f'<strong>{num.split()[0]}</strong>'
        last = num.split()[1]
        if last == '유지':
            rank += '<br><small>-</small>'
        elif last.find('상승') > 0:
            rank += f'<br><small><span style="color: red;">▲{last[:-2]}</span></small>'
        else:
            rank += f'<br><small><span style="color: blue;">▼{last[:-2]}</span></small>'
        ''' title = tr.select_one('a.title').string.strip()
        artist = tr.select_one('a.artist').string
        album = tr.select_one('a.albumtitle').string '''
        title = tr.select_one('.title.ellipsis').get_text().strip()
        artist = tr.select_one('.artist.ellipsis').get_text().strip()
        album = tr.select_one('.albumtitle.ellipsis').get_text().strip()
        img = 'https:' + tr.select_one('a.cover').find('img').attrs['src']
        music_list.append({'index':index, 'rank':rank, 'title':title, 'artist':artist,
                            'album':album, 'img':img})
    return music_list

def interpark():
    url_base = 'http://book.interpark.com'
    url_sub = '/display/collectlist.do?_method=bestsellerHourNew&bookblockname=b_gnb&booklinkname=%BA%A3%BD%BA%C6%AE%C1%B8&bid1=w_bgnb&bid2=LiveRanking&bid3=main&bid4=001'
    url = url_base + url_sub
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    lis = soup.select_one('.rankBestContentList ').select('.listItem.singleType')

    book_list = []
    for index, li in enumerate(lis):
        rank = index + 1
        title = li.select_one('.itemName').string.strip()
        author = li.select_one('.author').string
        company = li.select_one('.company').string
        price = li.select_one('.price').find('em').string
        href = url_base + li.select_one('.coverImage').find('a').attrs['href']
        img = li.select_one('.coverImage').find('img').attrs['src']
        book_list.append({'rank':rank, 'title':title, 'author':author,
                          'company':company, 'price':price, 'href':href, 'img':img})
    return book_list

def convert_unit(s):
    s = s.replace('억', '').replace('개','').replace(',','')
    s = s.replace('만', '0000')
    return f'{int(s):,d}'

def youtube():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')   # 화면없이 실행
    options.add_argument('--no-sandbox')
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome('chromedriver', options=options)
    
    url = 'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page=1'
    driver.get(url)
    time.sleep(2)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    channel_list = soup.select('.aos-init')
    results = []
    for channel in channel_list:
        rank = channel.select_one('.rank').text.strip()
        category = channel.select_one('p.category').get_text().strip(' \n[]')
        name = channel.select_one('.subject a').text.strip()
        subscriber = convert_unit(channel.select_one('.subscriber_cnt').text)
        view = convert_unit(channel.select_one('.view_cnt').text)
        video = convert_unit(channel.select_one('.video_cnt').text)
        results.append({'rank':rank, 'category':category, 'name':name, 
                        'subscriber':subscriber, 'view':view, 'video':video})
    return results