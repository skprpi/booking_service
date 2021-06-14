from django.urls import path

from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='user_logout'),
    path(
        'select_discipline/<int:teacher_pk>/',
        select_discipline, name='select_discipline'),
    path(
        'select_discipline/<int:teacher_pk>/ajax/get_discipline/',
        get_discipline, name='get_discipline', ),
    path(
        'select_discipline/<int:teacher_pk>/ajax/get_lessons/',
        get_lessons, name='get_lessons', ),
    path(
        'select_discipline/<int:teacher_pk>/ajax/make_db_note/',
        make_db_note, name='make_some3', ),
    path(
        'time_table/ajax/cancel_lesson/',
        cancel_lesson, name='cancel_lesson', ),
    path('time_table/', get_timetable, name='get_timetable'),
]
