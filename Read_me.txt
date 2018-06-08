----------------------------------------성분표 분석 DB 크롤링---------------------------------------------

기본적으로 python 크롤링을 위해 설치해야 하는 것

1)
cmd 에서 cd 명렁어를 통해 python이 저장 된 경로를 설정한다.

2) 입력
pip install pymysql
pip install BeautifulSoup4
pip install Selenium


-----------------------------------------------Manual------------------------------------------------------

1. 셀레니움을 통한 크롤링을 위해서 chromedriver.exe 가 필요하다.(git에 올려져있음) 
(다른 driver를 쓰고 싶다면 코드를 수정 할 필요가 있음)

2. Create_Table.sql을 mysql로 실행시켜 테이블은 만든다.

3. 크롤링.py 실행하기 위해 프로그램 안 DB 연결 코드의 일부분을 변경 할 필요가 있다.

Ex)	conn = pymysql.connect(host='localhost', user='root',
                       password='1111',db='food_additive', charset='utf8'
                       )
위의 코드에서 password에 자신의 DB 비밀번호를 입력해야 함


4. 마지막으로 크롤링을 성공적으로 마친 후 db에 입력 됬다면 update.sql을 실행하여 주의성분을 추가 수정한다.

5. 완성된 db를 가지고 성분표 분석을 시작한다.

------------------------------------------------SQL--------------------------------------------------------

DB table은 food_additive를 가진다.

food_additive("이름명","주요용도","EWG 등급","주의사항","10대 위험물질분류")