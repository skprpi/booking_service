from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('home/<int:pk>/', home, name='home'),
    path('home2/<int:teacher_pk>/', home2, name='home2'),
]
