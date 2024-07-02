# account/urls.py

from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("join", views.create, name="join"),
]
# http://ip:port/account/join  -> views.create