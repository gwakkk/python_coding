from selenium import webdriver
from bs4 import BeautifulSoup
import time, os
from datetime import datetime
import pandas as pd

# 명지대학교 도서관 리뷰 크롤러만들기
link = 'https://play.google.com/store/apps/details?id=kr.ac.mjlib.library&hl=ko&showAllReviews=true'

# 20번 스크롤
scroll_cnt = 10

#driver = webdriver.Chrome('./chromedriver')
driver = webdriver.Chrome('/Users/chan/Desktop/Git Upload/py_coding/auto_crawler/chromedriver.exe')
driver.get(link)

os.makedirs('result', exist_ok=True)

for i in range(scroll_cnt):
  driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  # JS를 실행(document의 body만큼 스크롤 : 맨 밑으로 향하게 된다.)
  time.sleep(3)

  # 리뷰 더보기 버튼이 있는 경우 클릭
  try:
    load_more = driver.find_element_by_xpath('//*[contains(@class,"U26fgb O0WRkf oG5Srb C0oVfc n9lfJ")]').click()
    # driver.find_element_by_xpath() : xml에서 노드의 위치를 찾기 위해 사용
  except:
    print('클릭할 더보기 버튼이 없습니다')

# jsname = "fk8dg"인 것중 class가 "d15Mdf bAhLNe"인 것을 찾는다.
# 각각의 리뷰를 찾는 것
reviews = driver.find_elements_by_xpath('//*[@jsname="fk8dgd"]//div[@class="d15Mdf bAhLNe"]')

print('There are %d reviews avaliable!' % len(reviews))
print('Writing the data...')

# 리뷰데이터를 dataframe형태로 저장
df = pd.DataFrame(columns=['name', 'ratings', 'date', 'helpful', 'comment', 'developer_comment'])

for review in reviews:
  # bs4를 이용한 파싱
  # review.get_attribute('innerHTML') : HTML을 텍스트형태로 받아온다.
  soup = BeautifulSoup(review.get_attribute('innerHTML'), 'html.parser')

  name = soup.find(class_='X43Kjb').text
  # strip은 공백 삭제
  ratings = int(soup.find('div', role='img').get('aria-label').replace('별표 5개 만점에', '').replace('개를 받았습니다.', '').strip())

  # 리뷰 데이터
  date = soup.find(class_='p2TkOb').text
  date = datetime.strptime(date, '%Y년 %m월 %d일')
  date = date.strftime('%Y-%m-%d')

  # 추천 / 추천이 존재하지 않는 경우는 0점으로 대체
  helpful = soup.find(class_='jUL89d y92BAb').text
  if not helpful:
    helpful = 0
  
  # 리뷰 본문
  comment = soup.find('span', jsname='fbQN7e').text
  if not comment:
    comment = soup.find('span', jsname='bN97Pc').text
  
  # 개발자 답변
  developer_comment = None
  dc_div = soup.find('div', class_='LVQB0b')
  if dc_div:
    developer_comment = dc_div.text.replace('\n', ' ')
  
  df = df.append({
    'name': name,
    'ratings': ratings,
    'date': date,
    'helpful': helpful,
    'comment': comment,
    'developer_comment': developer_comment
  }, ignore_index=True)

# dataframe을 csv 형태로 변환하여 저장
filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
df.to_csv(filename, encoding='utf-8-sig', index=False)
driver.stop_client()
driver.close()

print('크롤링 완료')