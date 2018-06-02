import pymysql        #mysql과 python의 연동
import urllib.request #url의 html을 불러오기 위함
from bs4 import BeautifulSoup
from selenium import webdriver

target_url="http://www.foodsafetykorea.go.kr/portal/safefoodlife/foodAditive/foodAdditiveBasisInfo.do?page_gubun=2&procs_cl=1&keyfield=adtv_nm&key=&page=%d"

def fetch_food_additive(html):
    bs=BeautifulSoup(html,'html.parser')
    article_tag=bs.find('article') #article tag를 가져오기 위함
    contents=article_tag.find('ul',class_='bs-underline02').get_text('/',strip=True)
    lists=contents.split("/")
    return lists

for i in range(1,22,1):
    res=urllib.request.urlopen(target_url %i)
    html=res.read()
    if(i==1):
        food_additive=fetch_food_additive(html)
    else:
        food_additive+=fetch_food_additive(html)

print(food_additive)
