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


conn = pymysql.connect(host='localhost', user='root',
                       password='1111',db='food_additive', charset='utf8'
                       )

try:
    cur = conn.cursor()
    for link in food_additive:
        cur.execute('insert into food_additive values(''%s'',null,null)' %link) #execute 안에 쿼리문을 입력

    #rows = cur.fetchall() # 전부 가져옴
    #for data in rows:
    #    print(data)

finally:
    cur.close()  #cur을 먼저 종료하고
    conn.close() #conn을 종료

