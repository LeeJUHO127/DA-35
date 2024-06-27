# polls/models.py
## Model class 정의
## django.db.models.Model 상속
## class 변수로 컬럼과 연결된 변수(Field)를 선언

from django.db import models

# Question Model 클래스 (질문)
class Question(models.Model): # table생성
    # 변수명 - 컬럼명
    # Field 객체(설정) - 컬럼 데이터 타입 (제약조건)
    question_text = models.CharField(max_length=200)  # 문자열 타입 컬럼(varchar(200))
    pub_date = models.DateTimeField(auto_now_add=True)# 날짜/시간타입 (datetime) - auto_now_add=True: insert할 때 일시를 저장.
    def __str__(self):
        return f"{self.id}. {self.question_text}"

# Choice Model class (보기)
class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes =  models.IntegerField(default=0) # 몇명이 선택했는지 값. default=0 -> insert할 때 값을 넣지 않으면 0을 insert.
    ## 부모테이블을 참조하는 Foreign key 컬럼 (Question의 PK 컬럼)
    question = models.ForeignKey(
        Question, # 참조 모델클래스 
        on_delete=models.CASCADE  # 참조 값이 삭제될때 처리방법.
        # , related_name = "polls_choice_set"  
    )
    def __str__(self):
        return f"{self.id}. {self.choice_text}"
    