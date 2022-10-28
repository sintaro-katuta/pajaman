# redirect使いたいときコメント外す
# from django.shortcuts imoprt redirect
# ここにfrom import
from email.policy import default
from django.forms import ModelChoiceField
from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic import *
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import *


# Create your views here.

# ホーム
class HomeView(TemplateView):
    template_name = "pajamanApp/home.html"

# 新規登録
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "pajamanApp/SignUp.html"
    success_url = reverse_lazy("pajamanApp:main")

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

# ログイン
class LoginView(LoginView):
    form_class = LoginForm
    template_name = "pajamanApp/login.html"

# ログアウト
class LogoutView(LoginRequiredMixin,LogoutView):
    template_name = "pajamanApp/home.html"

# メイン
class MainView(LoginRequiredMixin,TemplateView):
    template_name = "pajamanApp/main.html"
    login_url = "/"

# 企業分析
class CompanyView(LoginRequiredMixin,TemplateView):
    template_name = "pajamanApp/company.html"
    login_url = "/"

# 自己分析
class SelfView(LoginRequiredMixin,TemplateView):
    template_name = "pajamanApp/self.html"
    login_url = "/"

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('pajamanApp:password_change_done')
    template_name = 'pajamanApp/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context


class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'pajamanApp/password_change_done.html'

# --- ここから追加
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'pajamanApp/mail_template/reset/subject.txt'
    email_template_name = 'pajamanApp/mail_template/reset/message.txt'
    template_name = 'pajamanApp/password_reset_form.html'
    success_url = reverse_lazy('pajamanApp:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'pajamanApp/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('pajamanApp:password_reset_complete')
    template_name = 'pajamanApp/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'pajamanApp/password_reset_complete.html'
