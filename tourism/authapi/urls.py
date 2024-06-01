# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('user_profile', views.user_profile,
         name='user_profile'),
    path('admin_dashboard', views.admin_dashboard,
         name='admin_dashboard'),
]
