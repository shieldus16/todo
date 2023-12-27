from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.calendar, name='calendar'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]