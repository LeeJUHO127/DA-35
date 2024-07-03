1. project 생성
   1. django-admin  startproject  mypolls  (프로젝트이름)
   2. project directory를 생성하고 그 안으로 들어가서 실행.
      1. mkdir mypolls   (프로젝트 디렉토리 생성)
      2. cd mypolls
      3. django-admin  startproject  config   . 
         1. config: 설정파일들 저장할 디렉토리명.
2. 개발 (웹) 서버 실행
   1. python manage.py runserver
   2. web browser에서 `http://127.0.0.1:8000`  호출
3. App 생성. (app이름: polls)
   1. `python  manage.py  startapp  polls`
   2. config\settings.py
      1. INSTALLED_APPS 에 APP명(polls)을 등록
      2. LANGUAGE_CODE = 'ko-kr', TIME_ZONE = 'Asia/Seoul'
   3. config\urls.py
      1. urlpatterns에 path("app이름/", include("app이름.urls")
      2. app폴더\urls.py 를 생성. (polls\urls.py)
4. 관리자 계정(superuser) 생성
   1. 이 프로젝트(web application)의 관리자 계정.
   2. `python manage.py  migrate`
   3. `python manage.py createsuperuser`
      1. username(root), email:a@a.com, password(1111)
   4. 서버를 실행(python manage.py runserver)
   5. http://127.0.0.1:8000/admin

## Model 클래스 정의
1. models.py에 모델클래스들 정의
2. admin app에서 데이터를 관리하려는 경우
   1. admin.py 에 정의한 모델클래스를 등록
3. Database에 적용(모델클래스 추가, 변경.)
   1. `python manage.py makemigrations` 
      1. 테이블생성/수정 SQL문 생성.
   2. `python manage.py migrate`
      1. DB에 적용.

## View 구현
- View는 사용자 요청당 한개씩 정의(함수, 클래스)
1. app/views.py 에 작성
   1. 함수(FBV) 또는 클래스(CBV) 로 정의
2. app/urls.py 에 view를 등록
   1. 어떤 요청 들어오면 view를 호출할지 설정.
3. app/templates 에 template을 작성
   1. template: 응답 페이지. (view함수에서 호출.)

- polls/urls.py(요청경로-view), polls/views.py(view정의) -> open
- template:  polls/templates/polls 하위에 template파일을 작성.

## Template
- Template 파일을 저장하는 경로.
  - app/templates  하위에 저장. (이 디렉토리는 장고 실행환경이 자동으로 인식하는 경로. => 다른 설정 없이 이 아래 파일들은 바로 호출가능.)
    - 호출: app/templates 다음 하위경로부터 지정.
    - app/templates/test.html -> "test.html"
    - app/templates/app/src.html -> "app/src.html"
  - project 하위에 templates 들을 저장.
    - 특정 app을 위한 화면이 아니라 project 와 관련된 화면일 경우.
    - config/settings.py (프로젝트 설정파일) 에 등록
      - TEMPLATES.DIRS 딕셔너리에 추가.
      - app/templates 를 제외한 나머지 templates 저장 디렉토리들을 등록.

# template
- 특정 app 포함되지 않는 template 들을 저장할 디렉토리.
  1. root 디렉토리 아래 저장할 경로를 만들고 전역설정파일 config/settings.py 에 등록
     -  TEMPLATES/DIRS
  2. config/templates 생성(자동인식) 


## 사용자 계정 관리

1. 계정관리 app 생성
   1. `python manage.py startapp account`
   2. config.urls - account url 매핑
   3. account/urls.py
   4. config.settings - INSTALLED_APP에  accout app등록
2. 사용자 정의 User 모델클래스를 작성
   1. account/models.py
   2. account/admin.py  에 등록 (관리자 앱에서 관리할 수있도록 등록.)
   3. config/settings.py 모델에 작성한 AbstractUser 를 등록 (시스템에서 사용하는 User모델을 우리가 만든 모델 클래스로 변경.)
      1. AUTH_USER_MODEL = "account.모델클래스이름"
   4. DB에 적용
      1. python manage.py makemigrations
      2. python manage.py migrate
      3. 관리자 계정 생성
         1. python manage.py createsuperuser
   5. account/templates/account 디렉토리 생성



# django-bootstrap5
- django template에 bootstrap 을 추가해주는 library
- {{form}} 대신 사용.
  - `pip install django-bootstrap5`
  - config.setting : INSTALLED_APP 에 `django_bootstrap5`
  - django_bootrap이 제공하는 template 태그들을 로딩
    - {% load django_bootstrap5 %}