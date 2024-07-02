from django.db import models
from django.contrib.auth.models import AbstractUser
# 확장 User모델 정의
## AbstractUser 상속 (장고가 제공하는 User 모델과 연동.)

class User(AbstractUser):
    # Field(table attribute)를 설정
    ## username, password -> AbstractUser에 정의되어 있으므로 선언안함.
    ##    추가 field들을 정의
    name = models.CharField(verbose_name="이름", max_length=50)
    email = models.EmailField(verbose_name="Email", max_length=100)
    birthday = models.DateField(
        verbose_name="생일",
        null=True,    # NULL을 허용하는 컬럼. (default: False)
        blank=True,   # null의 상태와 동일 지정.(default: False)
        )
    # 파일 - 이미지파일.
    # profile_img = models.ImageField(
    #     verbose_name="프로필사진", 
    #     upload_to="images/%Y/%m/%d", # 업로드된 파일 저장할 디렉토리. 패턴문자(%Y%m%d) - 업로드된 날짜 디렉토리에 저장.
    #     null=True, blank=True
    # )
    def __str__(self):
        return self.name
