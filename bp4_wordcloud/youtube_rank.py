from selenium import webdriver
from bs4 import BeautifulSoup
import time, sys
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')   # 화면없이 실행
options.add_argument('--no-sandbox')
options.add_argument("--single-process")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome('chromedriver', options=options)

# 만과 억을 숫자로 바꿔주는 함수
def convert_unit(s):
    s = s.replace('억', '').replace('개','').replace(',','')
    s = s.replace('만', '0000')
    return f'{int(s):,d}'

# python youtube_rank.py [100 | 1000]
if len(sys.argv) == 1 or sys.argv[1] == '100':
    url = 'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page=1'
    driver.get(url)
    time.sleep(2)
    #trs = driver.find_elements_by_css_selector('.aos-init')
    #print(len(trs))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    channel_list = soup.select('.aos-init')
    print(f'Channel list 갯수: {len(channel_list)}')

    results = []
    for channel in channel_list:
        category = channel.select_one('p.category').get_text().strip(' \n[]')
        name = channel.select_one('.subject a').text.strip()
        subscriber = convert_unit(channel.select_one('.subscriber_cnt').text)
        view = convert_unit(channel.select_one('.view_cnt').text)
        video = convert_unit(channel.select_one('.video_cnt').text)
        results.append([category,name,subscriber,view,video])

    df = pd.DataFrame(results, columns=['카테고리','채널명','구독자수','조회수','비디오수'])
    df.to_csv('youtube_rank_top_100.tsv', sep='\t', index=False)

else:
    results = []
    for page in range(1,11):
        print(page, 'page')
        url = 'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page='+str(page)
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        channel_list = soup.select('.aos-init')

        for channel in channel_list:
            category = channel.select_one('p.category').get_text().strip(' \n[]')
            name = channel.select_one('.subject a').text.strip()
            subscriber = convert_unit(channel.select_one('.subscriber_cnt').text)
            view = convert_unit(channel.select_one('.view_cnt').text)
            video = convert_unit(channel.select_one('.video_cnt').text)
            results.append([category,name,subscriber,view,video])

    df = pd.DataFrame(results, columns=['카테고리','채널명','구독자수','조회수','비디오수'])
    df.to_csv('youtube_rank_top_1000.tsv', sep='\t', index=False)

driver.close()
