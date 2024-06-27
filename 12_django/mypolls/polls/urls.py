# polls/urls.py
from django.urls import path
# views.py 모듈을 import
from . import views 


# app 이름을 등록(설정)
## 이 설정파일의 설정을 외부에서 호출 할 때 사용할 prefix
app_name = "polls"

urlpatterns = [
    # path("요청url경로", 실행할 view, name=이 설정의 이름)
    ## http://ip:port/polls/welcome -> views.welcome 호출
    path("welcome", views.welcome, name="welcome_poll"),
]
# http://ip:port/polls/welcome
# config.urls : http://ip:port/polls/
# polls.urls : welcome

# http://ip:port/polls/welcome ---> views.welcome 호출