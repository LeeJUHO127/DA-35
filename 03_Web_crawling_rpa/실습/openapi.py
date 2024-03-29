# open_api.py
## data.go.kr  (공공데이터 포털) 제공 open api 데이터 조회
## Open API 데이터 요청
### 1. 인증키 신청
### 2. 요청 방식을 확인 - URL, 요청파라미터
### 3. 결과 양식을 확인 - 값들이 어떤 이름으로 넘어오는지
###    - JSON, XML

import requests

url = 'http://apis.data.go.kr/1360000/MidFcstInfoService/getMidFcst'
params ={'serviceKey' : 'laglZqyWw2mLMtqjyw9zoItPpOt3ChysDk/RvZnvfD+ejQHlbetkWSrYTKrpBcgrYjRdW+MP5b6d7ArwHxVj4g==', 
        'pageNo' : '1', 
        'numOfRows' : '10', 
        'dataType' : 'JSON', 
        'stnId' : '108', 
        'tmFc' : '202403281800' }

response = requests.get(url, params=params)
result = response.json() # dict
print(type(result))
from pprint import pprint
# pprint(result)
print(result['response']['body']['items']['item'])
