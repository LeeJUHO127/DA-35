# polls/admin.py
from django.contrib import admin
from .models import Question, Choice
# .models  .:  현재 module이 있는 패키지.
## polls/models.py 의 Question, Choice 클래스를 import

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
