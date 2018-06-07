import pymysql        #mysql과 python의 연동
import urllib.request #url의 html을 불러오기 위함
from bs4 import BeautifulSoup
from selenium import webdriver

#selenium
try:
    driver = webdriver.Chrome('.\chromedriver.exe') # os.getcwd() 통해 확인한 경로에 chromedriver.exe 파일을 다운 받아야 합니다.
except:
    driver = webdriver.Chrome('.\chromedriver')

target_url='http://www.foodsafetykorea.go.kr/portal/safefoodlife/foodAditive/foodAdditiveBasisInfo.do?page_gubun=2&procs_cl=1&keyfield=adtv_nm&key=&page=%d'
use=[]
eng_name=[]
name=[]

for i in range(1,22,1):
    driver.get(target_url %i)
    res=urllib.request.urlopen(target_url %i)
    html=res.read()
    bs=BeautifulSoup(html,'html.parser')
    lists=bs.find('article').find('ul',class_='bs-underline02').find_all('li')
    for j in range(1,len(lists)+1,1):
        find_use=driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/article/div/div[3]/ul/li[%d]/a' %j)
        find_use.click()
        html=driver.page_source
        bs=BeautifulSoup(html,'html.parser')
        article_tag=bs.find('article')
        table_tag=article_tag.find('table',class_='bs-underline02',summary='품목별 정보')

        #['''''.''',주요용도,i want,''',''''']
        lists=table_tag.find('tbody').get_text('/',strip=True).split('/')

        k=0
        for i in range(0,len(lists),1):
            if(lists[i]=='주요용도'):
                use+=lists[i+1]
                print(lists[i+1])
            if(lists[i]=='식품첨가물영문명'):
                eng_name+=lists[i+1]
                print(lists[i+1])
            if(lists[i]=='식품첨가물명'):
                name+=lists[i+1]
                print(lists[i+1])
        

        driver.back()
