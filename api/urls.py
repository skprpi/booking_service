from django.urls import path
from api.views import *

urlpatterns = [
    path('lessons/', lessons_list),
    path('lessons/<int:pk>', lessons_detail),
]