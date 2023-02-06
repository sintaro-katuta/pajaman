# Create your models here.
import re
from time import timezone
from timeit import default_timer
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Personality(models.Model):
    name = models.CharField(max_length=5)
    def __str__(self):
        return self.name
    
class Question(models.Model):
    q_id = models.IntegerField(primary_key=True,verbose_name='質問ID')
    question = models.TextField(verbose_name='質問の内容')

    class Meta:
        verbose_name_plural = '質問'
        
    def __str__(self):
        return self.question

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,verbose_name='回答ID')
    answer = models.TextField(verbose_name='回答の内容')
    personality = models.ForeignKey(Personality,on_delete=models.CASCADE,verbose_name="性格")

    class Meta:
        verbose_name_plural = '回答'

    def __str__(self):
        return self.answer

class Self(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,verbose_name='質問')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='ユーザー')
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,verbose_name='回答')

    class Meta:
        verbose_name_plural = '自己分析'

    def __str__(self):
        return str(self.question)

class Company(models.Model):
    c_id = models.AutoField(primary_key=True,verbose_name="企業ID",blank=True)
    c_name = models.CharField(max_length=100,unique=True,verbose_name="企業名")


    class Meta:
        verbose_name_plural = '企業'
    
    def __str__(self):
        return str(self.c_name)

class CompanyAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="ユーザ名")
    company = models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="企業名")
    establishment = models.DateField(null=True,verbose_name="設立年月日",default="2000-01-01")
    location = models.CharField(null=True,max_length=50,verbose_name="所在地")
    capital = models.PositiveIntegerField(null=True,verbose_name="資本金")
    sales = models.PositiveIntegerField(null=True,verbose_name="売上高")
    emp_no = models.PositiveIntegerField(null=True,verbose_name="従業員数")
    representative = models.CharField(null=True,max_length=50,verbose_name="代表者")
    content = models.TextField(null=True,verbose_name="事業内容")
    url = models.CharField(null=True,max_length=50,verbose_name="参考url",default="https://")
    created_at = models.DateTimeField('登録日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)


    class Meta:
        verbose_name_plural = '企業分析'
    def __str__(self):
        return str(self.company)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    target = models.ForeignKey(CompanyAnalysis, on_delete=models.CASCADE, verbose_name='対象企業分析')
    text = models.TextField(verbose_name="コメント")
    created_at = models.DateTimeField('作成日', default=timezone.now)

    class Meta:
        verbose_name_plural = 'コメント'
    def __str__(self):
        return str(self.user)

class Like(models.Model):
    company_analysis = models.ForeignKey(CompanyAnalysis,on_delete=models.CASCADE,verbose_name="企業分析")
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="ユーザー")
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'いいね'
    def __str__(self):
        return str(self.user)
        
class ImageUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to="icon/")
    created_at = models.DateTimeField('登録日時', auto_now_add=True)
 
    class Meta:
        verbose_name_plural = 'アイコン'
    def __str__(self):
        return str(self.image)

class Personal(models.Model):
    personal = models.TextField(verbose_name='性格')
    
    class Meta:
        verbose_name_plural = '性格'
    def __str__(self):
        return str(self.personal)

