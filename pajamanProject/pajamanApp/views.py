# ここにfrom import
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *



# Create your views here.

# ホーム
class HomeView(TemplateView):
    template_name = "pajamanApp/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        return context

# 新規登録
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "pajamanApp/SignUp.html"
    success_url = reverse_lazy("pajamanApp:main")

    def form_valid(self,form):
        user = form.save()
        login(self.request,user,backend='django.contrib.auth.backends.ModelBackend')
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_analysis"] = CompanyAnalysis.objects.filter(user=self.request.user)
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        return context

# 企業リスト
class CompanyView(LoginRequiredMixin,ListView):
    model = CompanyAnalysis
    template_name = "pajamanApp/company_list.html"
    context_object_name = "company_list"
    success_url = reverse_lazy('pajamanApp:company_list')
    login_url = "/"

    def get_queryset(self):
        queryset = Company.objects.order_by('c_id','c_name')
        keyword = self.request.GET.get('keyword')

        if keyword:
            queryset = queryset.filter(Q(c_name__icontains=keyword))
            print(queryset)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        context["company_detail"] = CompanyAnalysis.objects.all
        context["company_form"] = CompanyForm(
            initial={
                "c_name": self.request.GET.get('keyword')
            })
        return context

    def post(self,arg):
        cname = self.request.POST.get('c_name')
        if cname:
            if not Company.objects.filter(c_name=cname):
                c_name = self.request.POST.get('c_name')
                Company.objects.create(c_name=c_name)
            else:
                error_msg = "すでに存在します"
                return HttpResponseRedirect(f"/company/?error={error_msg}")
        return HttpResponseRedirect("/company/")
        
# 企業分析内容
class CompanyAnalysisDetailView(LoginRequiredMixin,TemplateView):
    model = CompanyAnalysis
    template_name = "pajamanApp/company_analysis_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        context["company_analysis"] = CompanyAnalysis.objects.filter(pk=kwargs['pk'])
        context["comments"] = Comment.objects.order_by('-created_at').filter(target=kwargs['pk'])
        context["comment_form"] = CommentForm
        like_count = Like.objects.filter(company_analysis=kwargs['pk']).count()
        context['like_count'] = like_count
        if Like.objects.filter(user=self.request.user,company_analysis=kwargs['pk']).exists():
            context['is_user_liked'] = True
        else:
            context['is_user_liked'] = False
        return context
    
    def post(self,request,pk):
        if self.request.POST.get('text'):
            #ログインしているユーザー
            user = self.request.user
            #pkからcompany_analysisを取得
            company_analysis = CompanyAnalysis.objects.get(pk=self.kwargs['pk'])
            comment = request.POST.get('text')
            Comment.objects.create(user=user, target=company_analysis,text=comment)
        return HttpResponseRedirect("/company/analysis/")

# 企業分析作成
class CompanyAnalysisCreateView(LoginRequiredMixin,CreateView):
    model = CompanyAnalysis
    template_name = 'pajamanApp/company_detail_form.html'
    form_class = CompanyAnalysisForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        context['company'] = Company.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
       qryset = form.save(commit=False)
       # ログインしているユーザー
       user = self.request.user
       # pkからcompanyを取得
       company = Company.objects.get(pk=self.kwargs['pk'])
       qryset.user = user
       qryset.company = company
       qryset.save()
       return HttpResponseRedirect("/company/analysis/")

# 企業分析更新
class CompanyAnalysisUpdateView(LoginRequiredMixin,UpdateView):
    model = CompanyAnalysis
    fields = ("establishment", "location","capital","sales","emp_no","representative","content","url")
    template_name = "pajamanApp/company_detail_form.html"
    success_url = reverse_lazy('pajamanApp:company_analysis')
    login_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        context['company'] = Company.objects.get(pk=self.kwargs['pk'])
        return context

# 企業分析削除
class CompanyAnalysisDeleteView(LoginRequiredMixin,DeleteView):
    model = CompanyAnalysis
    template_name = "pajamanApp/company_delete.html"
    success_url = reverse_lazy('pajamanApp:company_analysis')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        return context


# 自分の企業分析
class CompanyAnalysisView(LoginRequiredMixin,ListView):
    model = CompanyAnalysis
    context_object_name = "company_analysis_list"
    template_name = "pajamanApp/company_analysis.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        context['company_analysis'] = CompanyAnalysis.objects.order_by('company').filter(user=self.request.user)
        return context

# 全体の企業分析
class CompanayAnalysisListView(LoginRequiredMixin,ListView):
    model = CompanyAnalysis
    template_name = "pajamanApp/company_analysis_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        context['company_analysis'] = CompanyAnalysis.objects.order_by('company').exclude(user=self.request.user)
        return context

    def get_queryset(self):
        queryset = CompanyAnalysis.objects.order_by('user','company')
        keyword = self.request.GET.get('keyword')
        sort = self.request.GET.get('-sort')

        if keyword:
            queryset = queryset.filter(Q(user__username__icontains=keyword))
        if sort:
            queryset = queryset.order_by(sort)
        return queryset

# いいね機能
def CompanyAnalysisLike(request):
    pk = request.POST.get('pk')
    context = {
    'user': f'{request.user.username}',
    }
    company_analysis = get_object_or_404(CompanyAnalysis,pk=pk)
    like = Like.objects.filter(company_analysis=pk,user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(company_analysis=company_analysis, user=request.user)
        context['method'] = 'create'

    context['like_count'] = Like.objects.filter(company_analysis=pk).count()
    return JsonResponse(context)


# 自己分析
class SelfView(LoginRequiredMixin,ListView):
    model = Self
    template_name = "pajamanApp/self_list.html"
    login_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        self_analysis = list(Self.objects.filter(user=self.request.user).all())
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        context["self"] = self_analysis
        return context



class SelfDetail(DetailView):
    model = Question
    template_name = "pajamanApp/self_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        context["answer"] = Answer.objects.order_by('answer').filter(question=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        answer_id = self.request.POST.get('answer')
        answer = Answer.objects.get(pk=answer_id)
        if self.kwargs['pk'] == 1:
            Self.objects.filter(user=self.request.user).delete()
        Self.objects.update_or_create(question=question,user=self.request.user,answer=answer)
        if self.kwargs['pk'] >= Question.objects.all().count():
            return HttpResponseRedirect("/self/list/")
        else:
            return HttpResponseRedirect(f"/self/{self.kwargs['pk']+1}/")

# パスワード変更
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('pajamanApp:password_change_done')
    template_name = 'pajamanApp/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context

# パスワード変更完了
class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'pajamanApp/password_change_done.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        return context

# パスワード変更
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'pajamanApp/mail_template/reset/subject.txt'
    email_template_name = 'pajamanApp/mail_template/reset/message.txt'
    template_name = 'pajamanApp/password_reset_form.html'
    success_url = reverse_lazy('pajamanApp:password_reset_done')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        return context

# パスワード変更完了
class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'pajamanApp/password_reset_done.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        return context
    
# 新パスワード
class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'pajamanApp/password_reset_confirm.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        return context

# 新パスワード完了
class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'pajamanApp/password_reset_complete.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        user = self.request.user
        context['icon'] = ImageUpload.objects.all().filter(user=user).order_by('-created_at').first()
        return context

#アイコン
def Icon(request):
    img = request.FILES['img-upload']
    user = request.user
    ImageUpload.objects.update_or_create(image=img, user=user)
    return HttpResponseRedirect("/main/")


