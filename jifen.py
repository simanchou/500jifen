#!/usr/bin/env python
# -*- coding: gbk -*-
# @Time       : 2018/1/4 20:06
# @Author     : 周星星 Siman Chou
# @Site       : https://github.com/simanchou
# @File       : jifen.py
# @Description:
from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import requests
import time

url = "http://liansai.500.com/zuqiu-4429/jifen-11734"

browser = webdriver.Chrome()
browser.get(url)
teamList = browser.find_element_by_id("one_team_select")
Select(teamList).select_by_value("1072")
time.sleep(2)
#score = browser.find_element_by_id("match_list_tbody")
#print(browser.page_source)
#print(score.text)
#headers = {
#'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
#}
#html = requests.get(url, headers=headers).content.decode("gbk")
##print(html)
#

html = browser.page_source

soup = BeautifulSoup(html, "html5lib")

title = soup.title.text
print(title)

scoreTable = soup.find("div", id="season_match_list").find("table")
#print(scoreTable)
tbody = scoreTable.find("tbody")
#print(tbody)
for tr in tbody.find_all("tr"):
    print("#" * 100)
    for td in tr.find_all("td"):
        if td.getText():
            print(td.getText())
            print(td.get_attribute("class"))