# daum_news_list 폴더의 csv 파일의 뉴스 링크를 이용해서
#  뉴스 상세 정보를 크롤링
#  뉴스 내용 (기자, 제목, ...)

# csv 파일을 읽기. 링크들만 조회
import pandas as pd

df = pd.read_csv(r"C:\Classes\DA-35\03_Web_crawling_rpa\실습\daum_news_list\2024-03-27-11-41-26.csv")
links = df['링크주소']
# print(links)
for link in links:
    print(link)