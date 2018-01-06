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
import time


def getPageSource(url, teamCode):
    # 进入浏览器设置
    options = webdriver.ChromeOptions()
    # 设置中文
    options.add_argument('lang=zh_CN.UTF-8')
    # 更换头部
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 '
        '(KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    teamList = browser.find_element_by_id("one_team_select")
    Select(teamList).select_by_value(teamCode)
    time.sleep(3)
    pageSource = browser.page_source
    browser.quit()
    return pageSource


def analyseDataFromPageSource(html):
    """
    :return: a list
    """
    soup = BeautifulSoup(html, "html5lib")

    scoreTable = soup.find("div", id="season_match_list").find("table")
    tbody = scoreTable.find("tbody")
    dataList = [('轮次', '比赛时间', '主队', '比分', '客队', '平均欧指', '赛果', '澳门盘口',  '盘路','大小', '历史交战')]
    for tr in tbody.find_all("tr"):
        tmpList = []
        for td in tr.find_all("td"):
            if td.getText():
                tmpList.append(td.getText())
        while len(tmpList) < 12:
            tmpList.insert(-2, "")
        tmpList.pop()
        if "." in tmpList[6]:
            _tmp = tmpList[6].split(".")
            first = "{}.{}".format(_tmp[0], _tmp[1][:2])
            second = "{}.{}".format(_tmp[1][2:], _tmp[2][:2])
            third = "{}.{}".format(_tmp[2][2:], _tmp[3])
            del tmpList[6]
            tmpList.insert(5, "{} {} {}".format(first, second, third))
        dataList.append(tuple(tmpList))
    return dataList


def generateExcel(data, teamName):
    import csv
    fileName = "{}.csv".format(teamName)
    with open(fileName, "w", newline="", encoding="utf-8") as c:
        cw = csv.writer(c, dialect="excel")
        cw.writerows(data)




if __name__ == "__main__":
    url = "http://liansai.500.com/zuqiu-4429/jifen-11734"
    teamDict = {
        "1072": "曼  城",
        "1075": "曼  联",
        "1173": "切尔西",
        "1011": "利物浦",
        "1238": "热  刺",
        "554": "阿森纳",
        "700": "伯恩利",
        "973": "莱切城",
        "565": "埃弗顿",
        "1274": "沃特福",
        "847": "哈德斯",
        "721": "布赖顿",
        "1137": "纽  卡",
        "516": "水晶宫",
        "1286": "西汉姆",
        "667": "伯恩茅",
        "1128": "南安普",
        "1197": "斯托克",
        "1284": "西布罗",
        "511": "斯旺西"
    }

    for teamCode, teamName in teamDict.items():
        print("开始采集【{}】的数据...".format(teamName))
        html = getPageSource(url, teamCode)
        data = analyseDataFromPageSource(html)
        generateExcel(data, teamName)
        print("【{}】的数据采集完成！".format(teamName))
        print("等待3秒继续...")
        time.sleep(3)
