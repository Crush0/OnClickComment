import sys

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# 一键评教
# 总体思路:
# 先用requests模块，获得所有课程评教的链接
# 然后用selenium评教


base_url = 'http://jwgl.just.edu.cn:8080'
login_url = base_url + '/jsxsd/xk/LoginToXk'
post_url = base_url + '/jsxsd/xspj/xspj_save.do'
session = requests.session()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 " \
             "Safari/605.1.15 "
options = webdriver.ChromeOptions()
options.add_argument('--user-agent=%s' % user_agent)


# 首先requests登录
def start(username, password):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        'USERNAME': username,
        'PASSWORD': password
    }
    session.post(login_url, headers=headers, data=urlencode(data), allow_redirects=False)
    return username, password


# 获得所有课程的评教链接
def getSubjectList():
    url = base_url + '/jsxsd/xspj/xspj_find.do'
    res = session.get(url)
    soup = BeautifulSoup(res.text, features="lxml")
    elements = soup.find_all("a", attrs={"title": "点击进入评价"})
    ret_ = []
    for element in elements:
        href = base_url + element.get('href')
        res_ = session.get(href)
        soup_ = BeautifulSoup(res_.text, features="lxml")
        a = soup_.find_all('a', text="评价")
        for a_ in a:
            ret_.append(base_url + a_.get('href').split('JsMod(\'')[1].split('\',')[0])
    url = base_url + '/jsxsd/xspj/xspj_list.do'
    res = session.get(url)
    soup = BeautifulSoup(res.text, features="lxml")
    elements = soup.find_all("a", attrs={"title": "点击进入评价"})
    for element in elements:
        href = base_url + element.get('href')
        res_ = session.get(href)
        soup_ = BeautifulSoup(res_.text, features="lxml")
        a = soup_.find_all('a', text="评价")
        for a_ in a:
            ret_.append(base_url + a_.get('href').split('JsMod(\'')[1].split('\',')[0])
    return ret_


# 开始评教
def startComment(hrefs, user_):
    if len(hrefs) == 0:
        print('你没有需要评教的课程')
        exit(0)
    driver = webdriver.Chrome(options=options, executable_path=".\\chromedriver.exe")
    driver.get('http://jwgl.just.edu.cn:8080/jsxsd/')
    wait = WebDriverWait(driver, 10, 0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"Form1\"]/div/div/div[2]/div[1]/div[2]/input[1]")),
               message="")
    driver.find_element(by=By.XPATH, value="//*[@id=\"Form1\"]/div/div/div[2]/div[1]/div[2]/input[1]").send_keys(
        user_[0])
    driver.find_element(by=By.XPATH, value='//*[@id="pwd"]').send_keys(user_[1])
    driver.find_element(by=By.XPATH, value="//*[@id=\"btnSubmit\"]").click()
    wait.until(EC.presence_of_element_located((By.ID, "Top1_divLoginName")), message="")
    for href in hrefs:
        driver.get(href)
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="pj0601id_2_1"]').click()
        except:
            pass
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="pj0601id_3_1"]').click()
        except:
            pass
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="pj0601id_1_1"]').click()
        except:
            pass
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="pj0601id_4_2"]').click()
        except:
            pass
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="pj0601id_5_1"]').click()
        except:
            pass
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="pj0601id_1_2"]').click()
        except:
            pass
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="pj0601id_4_1"]').click()
        except:
            pass
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="tj"]').click()
        except:
            pass
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()


# 使用方式 python main.py 学号 教务系统密码
if len(sys.argv) != 3:
    print('启动参数错误')
    exit(0)
user = start(sys.argv[0], sys.argv[1])
ret = getSubjectList()
startComment(ret, user)
session.close()
