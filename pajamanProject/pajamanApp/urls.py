from django.urls import path ,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static




app_name = "pajamanApp"

urlpatterns = [
path("",views.HomeView.as_view(),name="home"),
    path("sign_up/",views.SignUpView.as_view(),name="sign_up"),
    path("main/", views.MainView.as_view(),name="main"),
    path('company/', views.CompanyView.as_view(), name='company'),
    path('company/analysis/',views.CompanyAnalysisView.as_view(), name='company_analysis'),
    path('company/analysis/list/', views.CompanayAnalysisListView.as_view(), name='company_analysis_list'),
    path('company/analysis/<int:pk>/',views.CompanyAnalysisDetailView.as_view(), name='company_analysis_detail'),
    path('company/like/',views.CompanyAnalysisLike, name='company_analysis_like'),
    path('company/analysis/create/<int:pk>/', views.CompanyAnalysisCreateView.as_view(), name='company_analysis_create'),
    path('company/update/<int:pk>/', views.CompanyAnalysisUpdateView.as_view(), name='company_analysis_update'),
    path('company/delete/<int:pk>/', views.CompanyAnalysisDeleteView.as_view(), name="company_analysis_delete"),
    path('self/<int:pk>/',views.SelfDetail.as_view(),name='self'),
    path('self/list/',views.SelfView.as_view(),name="self_list"),
    path('login/',views.LoginView.as_view(),name="login"),
    path('logout/',views.LogoutView.as_view(),name="logout"),
    path('password_change/',views.PasswordChangeView.as_view(),name="password_change"),
    path("image-upload/", views.Icon, name="image-upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

