from django.urls import path
from api.views import *

urlpatterns = [
    path('lessons/', LessonListView.as_view()),
    path('lessons/<int:pk>', LessonDetailView.as_view()),
]