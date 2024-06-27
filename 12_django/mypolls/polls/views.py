# polls/views.py
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# mypolls/polls/templates/polls/welocome.html

# View함수
def welcome(request):
    print("터미널에서 출력됩니다.")
    # return HttpResponse("안녕하세요. 환영합니다.")  # 반환값->클라이언트에 전달
    # templates을 호출해서 응답.
    response = render(
        request, 
        "polls/welcome.html", # template파일의 경로. app/templates 다음 부터 알려준다.
        {"my_name":"홍길동", "my_age":30} # tempate에 전달하는 값.
    )
    print(type(response))
    return  response