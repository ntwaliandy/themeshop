from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name="login"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    path('login_user', views.login_user, name="login_user"),
    path('reg_user', views.reg_user, name="reg_user"),
]