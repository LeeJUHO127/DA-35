# account/views.py
from django.shortcuts import render
from .models import User 

# 가입 처리
## GET  방식요청 - 입력폼을 응답
## POST 방식요청 - 가입 처리
####  - 요청파라미터 조회 -> 요청파라미터 검증 -> DB 저장 -> 응답(redirect)
def create(request):
    if request.method == "GET":
        return render(request, "account/join_form.html")
    elif request.method == "POST":
        # 요청파라미터 조회 - request.POST
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST["name"]
        email = request.POST["email"]
        birthday = request.POST["birthday"]
        print(username, password, name, email, birthday)
        
        # 검증 (등록된 username이 있는지 여부. password는 5글자 이상.)
        errorMessage = [] # 검증 실패시 에러메시지 저장.
        ## username중복 -> username으로 조회해서 있으면 중복
        user = User.objects.filter(username=username)
        if user.count() != 0:
            errorMessage.append("이미 사용중인 username입니다.")
        if len(password) < 5:
            errorMessage.append("패스워드는 5글자 이상 넣으세요.")

        if len(errorMessage) != 0: # 검증시 문제가 있다.
            return render(request, "account/join_form.html", 
                        {"error":errorMessage})
