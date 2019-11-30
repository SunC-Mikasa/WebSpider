from selenium import webdriver
import requests
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from selenium.webdriver.chrome.options import Options

i = 0

chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options = chrome_options)
bilibili_url = 'https://www.bilibili.com/anime/index/?spm_id_from=333.110.b_7375626e6176.7#season_version=-1&area=-1&is_finish=-1&copyright=1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1'

def process_bangumi(bangumi_href, num):
    try:
        page = pq(requests.get('https:' + bangumi_href, timeout = 20).text)
    except:
        return

    detail_page_url = page('.media-cover').attr('href')

    try:
        detail_page = pq(requests.get('https:' + detail_page_url, timeout = 20).text)
    except:
        return

    name = detail_page('.media-info-title-t').text()
    rating = detail_page('.media-info-score-content').text()
    play_time = detail_page('.media-info-count-item').text()
    intro = detail_page('.media-info-intro-text').text()
    try:
        browser.get('https:' + detail_page_url)
        intro = browser.find_element_by_class_name('media-info-intro-text').text
        browser.back()
    except:
        intro = 'An error occured when obtaining intro'

    info_string = name + '\n' + rating + '  ' + play_time + '\n'
    for tag in detail_page('.media-tag').items():
        info_string = info_string + tag.text() + '\t'
    info_string = info_string + '\n' + intro
    with open('bangumi.txt', 'a', encoding = 'utf-8') as f:
        f.write(str(num) + ' ')
        f.write(info_string + '\n' + '\n')


browser.get(bilibili_url)
a = 1
while i<100:
    bangumi_list = pq(browser.page_source)
    for bangumi in bangumi_list('.bangumi-list .bangumi-item').items():
        link = bangumi('.cover-wrapper').attr('href')
        process_bangumi(link, a)
        a += 1
    print('page ' + str(i+1) + ' processed')
    button = browser.find_element_by_class_name('next-page')
    button.click()
    i+=1
