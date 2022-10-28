from django.urls import path
from . import views



app_name = "pajamanApp"

urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("sign_up/",views.SignUpView.as_view(),name="sign_up"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("main/", views.MainView.as_view(),name="main"),
    path('company/', views.CompanyView.as_view(), name='company'),
    path('self/',views.SelfView.as_view(),name="self"),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'), #追加
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'), #追加
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'), #追加
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'), #追加
]
