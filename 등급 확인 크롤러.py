list='/foodscores/ingredients/7415-qwe/search'
url='https://www.ewg.org'

remove_search=list.split('/')
remove_search.remove('search')

k=''
for i in remove_search:
    k+=(i+'/')
	
// search 제거

// www.ewg.org 사이트는 urllib 크롤링을 거부하기에 셀레니움 사용

import re
import urllib.request #url의 html을 불러오기 위함
from bs4 import BeautifulSoup
from selenium import webdriver

try:
    driver = webdriver.Chrome('.\chromedriver.exe') # os.getcwd() 통해 확인한 경로에 chromedriver.exe 파일을 다운 받아야 합니다.
except:
    driver = webdriver.Chrome('.\chromedriver')

base_url="https://www.ewg.org"
url="https://www.ewg.org/foodscores/products?search=Sodium Nitrite"

driver.get(url)

html=driver.page_source

bs=BeautifulSoup(html,'html.parser')

tag=bs.find('ul',class_='double')

lists=tag.find_all('li')

for list in lists:
        r=re.search("Sodium Nitrite", "%s" %list)
        if(r!=None):
            link=re.search('href="(.*?)">','%s' %list).group(1)

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
    print('No concerns')
else:
    re.search('<strong>(.*?)</strong>',"%s" %concern).group(1)
	
// 등급을 받아오는 크롤링
