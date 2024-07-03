# account/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User 

from django.contrib.auth.decorators import login_required

# 가입 처리
## GET  방식요청 - 입력폼을 응답
## POST 방식요청 - 가입 처리
####  - 요청파라미터 조회 -> 요청파라미터 검증 -> DB 저장 -> 응답(redirect)
# def create(request):
#     if request.method == "GET":
#         return render(request, "account/join_form.html")
#     elif request.method == "POST":
#         # 요청파라미터 조회 - request.POST
#         username = request.POST['username']
#         password = request.POST['password']
#         name = request.POST["name"]
#         email = request.POST["email"]
#         birthday = request.POST["birthday"]
#         profile_img = request.FILES['profile_img'] #업로드 파일Field
#         print(username, password, name, email, birthday)
        
#         # 검증 (등록된 username이 있는지 여부. password는 5글자 이상.)
#         errorMessage = [] # 검증 실패시 에러메시지 저장.
#         ## username중복 -> username으로 조회해서 있으면 중복
#         user = User.objects.filter(username=username)
#         if user.count() != 0:
#             errorMessage.append("이미 사용중인 username입니다.")
#         if len(password) < 5:
#             errorMessage.append("패스워드는 5글자 이상 넣으세요.")

#         if len(errorMessage) != 0: # 검증시 문제가 있다.
#             return render(request, "account/join_form.html", 
#                         {"error":errorMessage, "name":name})
#         ## 검증 통과 
#         ### DB에 저장. 
#         user = User(username=username, 
#                     password=password, 
#                     name=name,
#                     email=email,
#                     birthday=birthday)
#         user.save() # insert
#         return redirect(reverse("home"))


# 가입 처리 - ModelForm을 이용
## GET  방식요청 - 입력폼을 응답
## POST 방식요청 - 가입 처리
from .forms import CustomUserCreateForm
def create(request):
    if request.method == 'GET':
        # context data 로 빈 Form(ModelForm) 객체를 template 전달.
        return render(
            request, 
            "account/create.html", 
            {"form":CustomUserCreateForm()}
        )
    elif request.method == "POST":
        # 요청파라미터 조회 -> 검증
        ### ModelForm/Form 에 요청파라미터를 넣어서 객체 생성.
        form = CustomUserCreateForm(request.POST, request.FILES)
        ## 검증 결과 이상이 없으면
        if form.is_valid():
            #정상처리 -> DB 저장 (ModelForm.save(): Model)
            user = form.save() # insert하고 insert한 값들을 가진 User(Model)객체를 반환
            ## 가입과 동시에 로그인
            login(request, user)            
            # 응답 : 등록->redirect방식
            return redirect(reverse('home'))
        else:
            # 요청파라미터 검증 실패. => 등록폼으로 이동.
            return render(request, "account/create.html",
                        {"form":form})  # form: 요청파라미터를 가진 Form

from django.contrib.auth import login, logout, authenticate       
# login(), logout(): 로그인/로그아웃 처리하는 함수
# authenticate(): username/password를 확인함수.
from django.contrib.auth.forms import AuthenticationForm 
#로그인 모델폼 - username, password 입력폼

### 로그인 처리: GET-로그인 폼반환, POST-로그인 처리
def user_login(request):
    if request.method == "GET":
        return render(request, 
                    'account/login.html', 
                    {"form":AuthenticationForm()})
    elif request.method == "POST":
        # 요청파라미터 조회
        username = request.POST['username']
        password = request.POST['password']
        ## AUTH_USER_MODEL를 기반으로 사용자 인증 처리
        ### 받은 username/password가 유효한 사용자 계정이라면 User객체를 반환.
        ###      유효하지 않은 사용자 계정이라면 None 반환.
        user = authenticate(request, username=username, password=password)
        if user is not None: # 유효한 사용자 계정.
            login(request, user) # 로그인 처리 -> 로그아웃할 때까지 request에 로그인한 사용자 정보를 사용할 수있도록 처리.
            return redirect(reverse("home"))
        else: # 유효한 사용자 계정이 아님
            return render(
                request,
                'account/login.html', 
                {"form":AuthenticationForm(), 
                "errorMessage":"ID나 Password를 다시 확인하세요."})

### 로그아웃 처리

# View를 실행할 때 로그인 되었는지를 먼저 체크.
## 로그인이 안되있으면 settings.LOGIN_URL  여기로 이동.
@login_required   
def user_logout(request):
    # login() 시 처리한 것들을 다 무효화시킴
    logout(request)
    return redirect(reverse('home'))

##### 로그인한 사용자 정보 조회
def user_detail(request):
    ## 로그인한 사용자 정보 -> request.user
    user = User.objects.get(pk=request.user.pk)
    return render(request, "account/detail.html", {"object":user})

##############
# 변경
##############

# 패스워드 변경 - GET: 폼제공, POST: 변경처리
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required 
def change_password(request):
    if request.method == "GET":
        # form = PasswordChangeForm(request.user)# 로그인한 User정보(old password 비교)
        form = CustomPasswordChangeForm(request.user)
        return render(
            request, "account/password_change.html", 
            {'form': form})
    elif request.method == "POST": # 패스워드 변경
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid(): #요청파라미터 검증이 잘 되었으면
            user = form.save()  # user의 password  update
            # 사용자의 정보(패스워드)가 변경된것을 session에 업데이트. 안하면 로그아웃이 된다.
            update_session_auth_hash(request, user) 
            return redirect(reverse("account:detail"))
        else: # 요청파라미터의 검증 실패
            return render(
                request, 'account/password_change.html',
                {'form':form, 'errorMessage':'패스워드를 다시 입력하세요.'}
            )

## 사용자 정보를 수정.
### GET - 수정폼(원래 입력값들이 폼필드에 나와야 한다.)
### POST - 수정처리 (로그인한사용자 정보 수정 -> session 정보를 update)

from .forms import CustomUserChangeForm
@login_required # 로그인한 사용자만 요청가능.
def user_update(request):
    if request.method == "GET":
        # User객체를 넣어서 생성. 
        ## 일반적인 수정의 경우는 DB에서 조회한 결과 Model객체를 넣어서 생성.
        ##### ItemForm(Item.object.get(pk=pk))
        form = CustomUserChangeForm(instance=request.user)
        return render(request, "account/update.html", {"form":form})
    elif request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # 저장, User 로그인 정보 갱신
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse('account:detail'))
        else:
            return render(request, "account/update.html", {"form":form})

# 탈퇴
@login_required  
def user_delete(request):
    # DB에서 user 정보 삭제 -> logout
    request.user.delete() # request의 user를 이용해 delete처리.
    # 일반적인 항목의 데이터를 DB에서 삭제 -> 
    #          삭제할 정보의 ID(path/request parameter)를 받아서 select 한 뒤에 삭제처리
    #  item = Item.objects.get(pk=pk)
    #  item.delete()

    # 삭제 후 로그아웃
    logout(request)
    return redirect(reverse('home'))

@login_required
def user_delete2(request, pk): # path parameter로 삭제할 Data의 pk 받기.
    # 조회해서 삭제
    user = User.objects.get(pk=pk)
    user.delete()
    logout(request)
    return redirect(reverse('home'))
