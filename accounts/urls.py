from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    # path('home/<int:teacher_pk>/', home, name='home'),
    path('select_discipline/<int:teacher_pk>/', select_discipline, name='select_discipline'),
    path('select_discipline/<int:teacher_pk>/ajax/data/', make_some, name='make_some'),
    path('select_discipline/<int:teacher_pk>/ajax/data2/', make_some2, name='make_some2'),
    path('select_discipline/<int:teacher_pk>/ajax/data3/', make_some3, name='make_some3'),
]
