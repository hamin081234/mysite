from django.db import models


# Create your models here.


class Question(models.Model):
    """질문 Question 클래스 생성: subject, content, create_date"""
    subject = models.CharField(max_length=200)  # 글자수 제한
    content = models.TextField()  # 글자수 제한이 없는 경우
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()  # 글자수 제한이 없는 경우
    create_date = models.DateTimeField()

    def __str__(self):
        return self.content

