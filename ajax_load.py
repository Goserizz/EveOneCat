from selenium import webdriver
import os
import time
from crawler_lib import scroll_to_bottom, get_tweet
from bs4 import BeautifulSoup
import json


os.environ['all_proxy'] = 'http://127.0.0.1:1087'
browser = webdriver.Chrome()
browser.get('https://twitter.com/motions_cat')
with open('motions_cat.json', mode='r') as f:
    cat_dict = json.load(f)

height = scroll_to_bottom(browser)
while True:
    time.sleep(1)
    height -= 500
    if height < 0:
        break
    browser.execute_script('window.scrollTo(0, {0})'.format(height))
    soup = BeautifulSoup(browser.page_source, features='lxml')
    now_list = get_tweet(soup)
    for i in range(0, len(now_list)):
        if now_list[i]['time'] not in cat_dict.keys():
            cat_dict[now_list[i]['time']] = now_list[i]
    print('\rRemains approx {0}s...'.format(int(browser.execute_script('return document.documentElement.scrollTop')) / 500), end='')

browser.close()

with open('motions_cat.json', mode='w') as f:
    json.dump(cat_dict, f)

for _time in cat_dict.keys():
    print(_time + ': ', end='')
    print(cat_dict[_time])
