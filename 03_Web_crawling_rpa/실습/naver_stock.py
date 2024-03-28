# naver_stock.py
# finance.naver.com (네이버 > 증권 > 국내증시 > 시가총액)
# 시가 총액 정보(표)의 내용을 크롤링
# (N(번호), 토론실 빼고 조회.)
# 삼성전자	80,100	상승 300	+0.38%	100	4,781,796	5,969,783	55.10	10,343,860	37.59	4.15	

# 1. URL ==> 페이지번호
#      : https://finance.naver.com/sise/sise_market_sum.naver?&page={NO}
#      : page번호: 1 ~ 44
# 2. 조회할 항목 -> SELECTOR
#      : TR Select: #contentarea > div.box_type_l > table.type_2 > tbody > tr
# 3. 저장방식 (CSV)
import time
import datetime
import os

import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

url_layout = "https://finance.naver.com/sise/sise_market_sum.naver?&page={}"
tr_selector = "#contentarea > div.box_type_l > table.type_2 > tbody > tr"

async def get_page_info(url, session):
    """
    naver stock 정보 개별 page url을 받아서 그 페이지의 내용을
    조회 코루틴.
    Return:
        list: 중첩 리스트로 정의. 
            한줄의 내용을 리스트로 묶고 그것들 모두 담은 리스트.
            [
                [td1, td2, ... , td11], # 1줄
                [td1, td2, ... , td11], # 2줄
                ...
            ]
    """
    async with session.get(url) as res:
        if res.status == 200:
            html = await res.text()
            soup = BeautifulSoup(html, 'lxml')
            # page내의 모든 tr(행들)들을 조회
            tr_list = soup.select(tr_selector)

            result_list = [] # 모든 행들의 정보를 담을 리스트.
            ## 개별 행(tr) 처리
            for tr in tr_list:
                # 개별 행(tr)안에 td들 조회
                td_list = tr.find_all("td")
                if len(td_list) == 1: # td가 1개인 tr -> 5개당 하나씩 나오는 선
                    continue
                tr_content_list = [] # 한행의 cell  정보(td들의 값)들을 담을 리스트.
                for idx, td in enumerate(td_list): # cell별로 따로 처리하는 것들이 있으므로 enumerate사용
                    if idx == 0 or idx == 12: # 첫번째(N), 마지막(토론식) 내용은 저장안함.
                        continue
                    txt = td.get_text().strip().replace(",", "") #쉼표제거
                    
                    ## 전일비. 이미지를 이용해서 상승인지 하락인지 조회.
                    if idx == 3:
                        # td 자식으로 이미지 태그 조회. (있으면 상한/하한, 없으면 보합)
                        img = td.find("img")
                        alt_txt = ""
                        if img != None: # 하위에 img 태그가 있으면
                            image_name = img.get("src") #image의 src 속성값
                            if image_name.endswith("ico_up.gif") or image_name.endswith('ico_up02.gif'):
                                alt_txt = "+"
                            else:
                                alt_txt = "-"
                        txt = alt_txt + txt
                    tr_content_list.append(txt)
                
                result_list.append(tr_content_list)
            return result_list

                    
async def main():
    """
    조회할 page들의 url을 이용해서 get_page_info 코루틴들을 
    생성해서 start
    결과를 취합해서 반환.
    """    
    async with aiohttp.ClientSession(headers={"user-agent":user_agent}) as session:
        result = await asyncio.gather(*[get_page_info(url_layout.format(page_no), session) for page_no in range(1, 45)])
    
    return result


if __name__ == "__main__":

    s = time.time()

    result = asyncio.run(main())

    e = time.time()
    print(f"걸린시간: {e-s}초")
    print(len(result))  # 44
    print(len(result[1])) # 50

    #### 받아온 결과를 파일로 저장
    #### stock_info/ 실행날짜.csv
    ## result 형태 (44, 50, 11) -> (페이지수, 페이지당 행수, 행당 컬럼수)
    #### 테이블 형태의 리스트로 만들기. (44, 50, 11) -> (44*50, 11)
    result_list = []
    for page_list in result:
        result_list += page_list

    column_name = ["종목명", "현재가", "전일비", "등락률", "액면가", "시가총액", "상장주식수", "외국인비율", "거래량", "PER", "ROE"]
    ## List -> DataFrame 
    df = pd.DataFrame(result_list, columns=column_name)

    ## 저장 디렉토리 생성
    os.makedirs('stock_info', exist_ok=True)
    ## 파일명 - %Y-%m-%d
    c_day = datetime.date.today().strftime("%Y-%m-%d")
    file_path = f"stock_info/{c_day}.csv"
    df.to_csv(file_path, index=False)
    print(">>>>>>>>>>완료<<<<<<<<<")


