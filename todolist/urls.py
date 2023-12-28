from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import get_todo, login, get_csrf_token


urlpatterns = [
    path('', views.calendar, name='calendar'),
    # path('login/', views.login, name='login'),
    path('api/login/', login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('api/todo/', get_todo, name='get_todo'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
]