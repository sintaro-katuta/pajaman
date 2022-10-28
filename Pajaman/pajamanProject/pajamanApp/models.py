# Create your models here.
from time import timezone
from timeit import default_timer
from django.db import models

class self_ass(models.Model):
    id = models.IntegerField(primary_key=True)
    s_text = models.TextField()
    s_image = models.CharField(max_length=255)
    s_creattime = models.DateTimeField('作成日時', auto_now_add=True)
    s_updetetime = models.DateTimeField('更新日時', auto_now=True)

class company_ass(models.Model):
    id = models.IntegerField(primary_key=True)
    c_text = models.TextField()
    c_image = models.CharField(max_length=255)
    c_creattime = models.DateTimeField('作成日時', auto_now_add=True)
    c_updetetime = models.DateTimeField('更新日時', auto_now=True)
    

    