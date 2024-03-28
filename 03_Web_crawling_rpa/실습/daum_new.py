# daum_news_list 폴더의 csv 파일의 뉴스 링크를 이용해서
#  뉴스 상세 정보를 크롤링
#  뉴스 내용 (기자, 제목, ...)

# csv 파일을 읽기. 링크들만 조회
import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup

article_selector = "#mArticle > div.news_view.fs_type1 > div.article_view > section > p"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

async def get_news(url, session):
    """
    개별 뉴스기사 내용을 조회하는 코루틴.
    Argument:
        url: str - 뉴스기사를 가져올 daum news url
        session: ClientSession - aiohttp session 
    Return:
        str: 조회한 뉴스기사
    """
    async with session.get(url) as res:
        if res.status == 200:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            p_list = soup.select(article_selector)
            article = [] # 뉴스기사 문단들을 저장할 리스트
            for p in p_list:
                article.append(p.get_text())
            # 리스트 안에 문단들을 하나의 string으로 합치기
            # "구분자문자열".join(리스트)
            return '\n'.join(article)
                

async def main(links):
    """
    get_news 코루틴들을 개별 기사 url별로 생성해서 task로 실행.
    Argument:
        links: list - 크롤링할 기사들의 url들.
    Return:
        list: 크롤링한 전체 기사들.
    """
    async with aiohttp.ClientSession(headers={"user-agent":user_agent}) as session:
        result = await asyncio.gather(*[get_news(url, session) for url in links])
    
    return result


if __name__ == "__main__":
    import time
    # 뉴스기사 링크들을 조회
    news_list_path = r"실습\daum_news_list\2024-03-28-09-39-00.csv"
    df = pd.read_csv(news_list_path)
    links = df['링크주소']

    s = time.time()
    result = asyncio.run(main(links)) # main 코루틴 실행.
    e = time.time()
    print(f"걸린시간: {e-s}초")
    print("기사개수:", len(result))
    # print(result[0])
    df['기사내용'] = result   
    # DataFrame(테이블-표) 기사내용 컬럼 추가. 그 컬럼의 값으로 result를 대입.
    # 데이터프레임의 내용을 csv 파일로 저장.
    df.to_csv(news_list_path, index=False)
    

