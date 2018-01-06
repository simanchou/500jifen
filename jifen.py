#!/usr/bin/env python
# -*- coding: gbk -*-
# @Time       : 2018/1/4 20:06
# @Author     : ������ Siman Chou
# @Site       : https://github.com/simanchou
# @File       : jifen.py
# @Description:
from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import time


def getPageSource(url, teamCode):
    # �������������
    options = webdriver.ChromeOptions()
    # ��������
    options.add_argument('lang=zh_CN.UTF-8')
    # ����ͷ��
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
    dataList = [('�ִ�', '����ʱ��', '����', '�ȷ�', '�Ͷ�', 'ƽ��ŷָ', '����', '�����̿�',  '��·','��С', '��ʷ��ս')]
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
        "1072": "��  ��",
        "1075": "��  ��",
        "1173": "�ж���",
        "1011": "������",
        "1238": "��  ��",
        "554": "��ɭ��",
        "700": "������",
        "973": "���г�",
        "565": "������",
        "1274": "���ظ�",
        "847": "����˹",
        "721": "������",
        "1137": "Ŧ  ��",
        "516": "ˮ����",
        "1286": "����ķ",
        "667": "����é",
        "1128": "�ϰ���",
        "1197": "˹�п�",
        "1284": "������",
        "511": "˹����"
    }

    for teamCode, teamName in teamDict.items():
        print("��ʼ�ɼ���{}��������...".format(teamName))
        html = getPageSource(url, teamCode)
        data = analyseDataFromPageSource(html)
        generateExcel(data, teamName)
        print("��{}�������ݲɼ���ɣ�".format(teamName))
        print("�ȴ�3�����...")
        time.sleep(3)
