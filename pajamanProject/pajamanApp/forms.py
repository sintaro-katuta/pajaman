from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from .models import *


class SignUpForm(UserCreationForm):

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ["username","email","password1","password2"]


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CompanyAnalysisForm(forms.ModelForm):
    class Meta:
        model = CompanyAnalysis
        fields = ("establishment","location","capital","sales","emp_no","representative","content","url")
        widgets = {
            'establishment': forms.SelectDateWidget(years=[x for x in range(1900, 2024)])
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("c_name",)
        widgets = {
            'c_name' : forms.TextInput(attrs={'placeholder': '企業名'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            'text' : forms.Textarea(attrs={'id': 'floatingTextarea','rows':4, 'cols':15,'style':'resize:none;'})
        }