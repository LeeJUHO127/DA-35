# polls/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

## paging 처리
from django.core.paginator import Paginator

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
    """
    Paging 처리.
    context data
        - 현재 페이지의 데이터 (Page객체)
        - 현재 페이지가 속한 page group의 시작페이지, 끝페이지 번호.
        - 시작 페이지의 이전/ 끝 페이지 다음 페이지가 있는지 여부.
        - 시작 페이지의 이전/ 끝 페이지 다음 페이지 번호        
    """
    paginate_by = 10 # Page당 데이터 개수.(한 페이지에서 몇개씩 보여줄지.)
    page_group_count = 10 # Page group 당 page수.
    
    # 사용자가 조회한 페이지(현재 페이지) - queryString (GET방식의 요청파라미터)
    ### http://127.0.0.1:8000/polls/list?page=3
    current_page = int(request.GET.get('page', 1))

    # DB에서 Question들 모두 조회 - Paging처리를 위해서는 정렬처리.
    question_list = Question.objects.all().order_by("-pk")
    # Paginator객체 생성 - (데이터들, 페이지당데이수)
    paginator = Paginator(question_list, paginate_by)

    # current_page 가 속한 page group의 시작 페이지, 끝 페이지 조회.
    start_idx = int((current_page - 1) / page_group_count) * page_group_count
    end_idx = start_idx + page_group_count

    page_range = paginator.page_range[start_idx : end_idx]

    # context data dictionry 에 template에 전달할 값들 추가.
    context_data = {
        "page_range": page_range,  # page group의 페이지 번호들
        "question_list": paginator.page(current_page), # Page객체
    }

    ### 현재 페이지가 속한 PageGroup의 시작/끝 페이지를 조회
    #### -> 시작페이지가 이전페이지가 있는지 여부, 이전페이지 번호
    #### -> 끝페이지가   다음페이지가 있는지 여부, 다음페이지 번호.
    start_page = paginator.page(page_range[0]) # Group 시작 Page객체
    end_page = paginator.page(page_range[-1])  # Group 끝 page객체
    # 시작 페이지가 이전 페이지가 있는지, 끝 페이지는 다음 페이지가 있는지 확인
    has_previous = start_page.has_previous()
    has_next = end_page.has_next()
    # 시작페이지가 이전 페이지가 있다면
    if has_previous:
        context_data['has_previous'] = has_previous
        context_data['previous_page_no'] = start_page.previous_page_number
    # 끝 페이지의 다음 페이지가 있다면
    if has_next:
        context_data['has_next'] = has_next
        context_data['next_page_no'] = end_page.next_page_number

    return render(request, "polls/list.html", context_data)





## 전체 데이터 조회
# def list(request):
#     """질문 목록(list)를 제공하는 View"""
#     # 1. DB에서 질문들 조회(전체조회) -> models.Question
#     question_list = Question.objects.all().order_by('-pub_date')
#     # 2. 질문 목록 화면 html을 정의 -> 반환
    
#     return render(
#         request, # HttpRequest(장고실행환경이 전달.-HTTP요청정보)
#         "polls/list.html", # 호출할 template파일의 경로.
#         {"question_list":question_list}, 
#         # Context Data: View가 Template에 전달하는 값. dictionary로 정의.
#     )
#     # render(HttpRequest, template경로, context_data): HttpResponse
#     ## template을 실행해서 응답할 html을 응답데이터로 만들어서 반환.

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
    question_id = request.POST.get('question_id')
    if choice_id: # 넘어온 값이 있다면
        # update할 choice를 조회
        choice = Choice.objects.get(pk=choice_id)
        # update field값을 변경
        choice.votes = choice.votes + 1
        # update
        choice.save() # pk가 db에 있으면 update, 없으면 insert

        # urls.py의 path 이름으로 url path를 조회.
        url = reverse("polls:vote_result",  # path name
                      args=[question_id])   # path parameter에 넣어줄 값
        print(url)
        return redirect(url) # 결과페이지로이동.
        # redirect방식으로 요청 - Web Browser가 전달한 url로 재요청하도록 응답
        #   - DB의 내용을 변경하는 요청(insert/update/delete) 을 처리할 경우 
        #     응답을 redirect 방식으로 해서 새로고침시 다시 처리되는 것을 막는다.
    else: # id가 넘어오지 않았다면.
        # 보기를 선택하지 않고 투표한 경우.
        
        question = Question.objects.get(pk=question_id)
        return render(
            request, 
            "polls/vote_form.html", 
            {"question":question, "error_message":"보기를 선택하세요."}
        )


def vote_result(request, question_id):
    """
    투표 결과를 보여주는 view함수.
    파라미터
        question_id: path parameter로 질문_id
    """
    question = Question.objects.get(pk=question_id)
    return render(
        request, "polls/vote_result.html", {"question":question}
    )

# 질문(+보기) 등록 페이지 보여주는 View
## 등록 양식 요청 - GET 방식 요청
## 등록 처리 요청 - POST 방식 요청
def vote_create(request):
    # HTTP 요청 방식을 조회
    print(request.method)
    if request.method == "GET":
        return render(request, "polls/vote_create_form.html")
    elif request.method == "POST":
        # 등록 처리.
        ## 1. 요청파라미터 조회 (질문, 보기들)
        ### GET방식: request.GET, POST방식: request.POST
        question_text = request.POST.get("question_text") #질문
        choice_list = request.POST.getlist("choice_text") # 보기들(같은이름으로 여러개가 넘어오는 경우 getlist())
        ## 2. 요청파라미터 검증 (글자수, 값이 넘어왔는지 ....)
        ## 3. 검증 통과 -> DB에 insert
        question = Question(question_text=question_text)
        question.save()
        for c_text in choice_list:
            choice = Choice(choice_text=c_text, question=question)
            choice.save()
        ## 4. 처리결과 응답 (성공-성공결과, 실패-실패결과)
        ### -> 질문 목록 이동. - redirect(); 새로고침시 계속 등록 되지 않도록 해야함.
        url = reverse("polls:list")
        return redirect(url)


