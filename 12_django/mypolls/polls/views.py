# polls/views.py
from django.shortcuts import render
from django.http import HttpResponse

# model class 들 import
from .models import Question, Choice

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

def list(request):
    """질문 목록(list)를 제공하는 View"""
    # 1. DB에서 질문들 조회(전체조회) -> models.Question
    question_list = Question.objects.all().order_by('-pub_date')
    # 2. 질문 목록 화면 html을 정의 -> 반환
    
    return render(
        request, # HttpRequest(장고실행환경이 전달.-HTTP요청정보)
        "polls/list.html", # 호출할 template파일의 경로.
        {"question_list":question_list}, 
        # Context Data: View가 Template에 전달하는 값. dictionary로 정의.
    )
    # render(HttpRequest, template경로, context_data): HttpResponse
    ## template을 실행해서 응답할 html을 응답데이터로 만들어서 반환.

# 설문에 응답
## 투표양식 응답.  
def vote_form(request, question_id):
    """
    투표양식을 응답.
    Path 파라미터(question_id)로 받은 id의 질문을 조회.
    양식화면을 만들어서 응답.
    """
    # get() : 조회결과 - Model(Question), 결과가 없으면 Exception발생
    try:
        question = Question.objects.get(pk=question_id)
        return render(
            request, "polls/vote_form.html",{"question":question}
        )
    except:
        print("없는 질문을 요청했습니다.")


# 요청파라미터 조회
## http 요청방식 GET - request.GET.get("요청파라미터이름" [, 기본값])
###                   request.GET["요청파라미터이름"]
## http 요청방식 POST - request.POST.get("요청파라미터이름" [, 기본값])
###                    request.POST["요청파라미터 이름"]
def vote(request):
    """투표 처리 view함수. (user가 선택한 보기의 votes를 1증가(update) 처리)"""
    # 요청파라미터로 전송된 choice의 id를 조회.
    choice_id = request.POST.get("choice") # 넘어온 값이 없으면 None
    if choice_id: # 넘어온 값이 있다면
        # update할 choice를 조회
        choice = Choice.objects.get(pk=choice_id)
        # update field값을 변경
        choice.votes = choice.votes + 1
        # update
        choice.save() # pk가 db에 있으면 update, 없으면 insert
        return 응답 tempate호출
        
    else: # id가 넘어오지 않았다면.
        print("보기를 선택하세요.")