from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    """질문 Question 클래스 생성: subject, content, create_date"""
    subject = models.CharField(max_length=200)  # 글자수 제한
    content = models.TextField()  # 글자수 제한이 없는 경우
    create_date = models.DateTimeField()
    # author 필드 추가: 글쓴이
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 회원테이블에 사용자 정보가 삭제 되면 Question 테이블 user도 모두 삭제
    modify_date = models.DateTimeField(null=True, blank=True)
    # 데이터 베이스에서 null 허용, form.is_valid() 입력값 검증시 값이 없어도 된다. blank = True

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()  # 글자수 제한이 없는 경우
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

