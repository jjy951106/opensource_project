import pymysql
import re
import urllib.request #url의 html을 불러오기 위함
from bs4 import BeautifulSoup
from selenium import webdriver

try:
    driver = webdriver.Chrome('.\chromedriver.exe') # os.getcwd() 통해 확인한 경로에 chromedriver.exe 파일을 다운 받아야 합니다.
except:
    driver = webdriver.Chrome('.\chromedriver')
##
target_url='http://www.foodsafetykorea.go.kr/portal/safefoodlife/foodAditive/foodAdditiveBasisInfo.do?page_gubun=2&procs_cl=1&keyfield=adtv_nm&key=&page=%d'
_use=[]
_eng_name=[]
_name=[]

c=0

for i in range(1,22,1): # page 21 까지 존재
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
                if(lists[i+1]=='JECFA 평가'):
                    _use.append('미표기')
                else:
                    _use.append(lists[i+1])
            if(lists[i]=='식품첨가물영문명'):
                _eng_name.append(lists[i+1])
            if(lists[i]=='식품첨가물명'):
                _name.append(lists[i+1])
        c+=1
        print(c)
        driver.back()
        
##
c=0        
_concern=[]

for _eng in _eng_name:

    base_url="https://www.ewg.org"
    url="https://www.ewg.org/foodscores/products?search=%s"

    driver.get(url %_eng)

    html=driver.page_source

    bs=BeautifulSoup(html,'html.parser')

    tag=bs.find('ul',class_='double')

    if(tag==None):
        _concern.append('등급 미표기')
        continue
    
    lists=tag.find_all('li')

    k=0
    if(len(lists)>1):
        for list in lists:
            change_search=_eng.replace(' ','').replace('-','').replace('δ','Delta')
            r=re.search(_eng, "%s" %list)
            if(r!=None):
                link=re.search('href="(.*?)">','%s' %list).group(1)
                k=1
                break
        if(k==0):
            for list in lists:
                change_search=_eng.replace(' ','').replace('-','').replace('δ','Delta').replace('α','Alpha').replace('β','Beta') #
                r=re.search(change_search.upper(), "%s" %list)
                if(r!=None):
                    link=re.search('href="(.*?)">','%s' %list).group(1)
                    k=1
                    break

    if(len(lists)==1):
        link=re.search('href="(.*?)">','%s' %lists).group(1)
        k=1
        
    if(k==0):
        _concern.append('등급 미표기')
        continue
    remove_search=link.split('/')
    remove_search.remove('search')

    k=''

    for i in remove_search:
        k+=(i+'/')
    
    base_url+=k

    driver.get(base_url)

    html=driver.page_source

    bs=BeautifulSoup(html,'html.parser')

    tag=bs.find('div',class_='content')
    concern=tag.find('p',style="margin: 15px 30px 0px 30px;")
    r=re.search("strong","%s" %concern)
    if(r==None):
        _concern.append('No Concerns')
    else:
        value=re.search('<strong>(.*?)</strong>',"%s" %concern).group(1)
        _concern.append(value+' Concerns')
    c+=1
    print(c)
    
##

conn = pymysql.connect(host='localhost', user='root',
                       password='1111',db='food_additive', charset='utf8'
                       )

try:
    cur = conn.cursor()
    for i in range(0,len(_name),1):
        cur.execute('insert into food_additive values("%s","%s","%s",null,0)' %(_name[i],_use[i],_concern[i]))
        #execute 안에 쿼리문을 입력

finally:
    conn.commit() # 작업을 db로 넘기는 명령.
    cur.close()  #cur을 먼저 종료하고
    conn.close() #conn을 종료


