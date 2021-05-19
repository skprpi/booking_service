from django.urls import path
from api.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('lessons', LessonViewSet, basename='lessons')
router.register('users', UserViewSet, basename='users')
urlpatterns = router.urls

# urlpatterns += [
#     path('lessons/', lessons_list, name='lessons-list'),
#     path('lessons/<int:pk>', lessons_detail, name='lessons-detail'),
# ]