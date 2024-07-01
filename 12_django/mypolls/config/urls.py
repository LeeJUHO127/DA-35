"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include("polls.urls")),
    path('account/', include('account.urls')),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]
### TemplateView: 단순히 template을 응답할 경우 사용.(응답할 template 경로만 지정.)
# http://ip:port/admin/ 그 이후 경로는 -> admin app의 urls.py 를 확인
# http://ip:port/polls/ 그 이후 경로는 -> polls/urls.py  를 확인
# http://ip:port/   ==> home.html 응답.

# http://127.0.0.1:8000/polls/  welcome -> welcome은 polls/urls.py를 확인해서 View를 찾는다.