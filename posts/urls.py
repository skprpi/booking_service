from django.urls import path

from . import views

urlpatterns = [
    path('follow/', views.follow_index, name='follow_index'),
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group'),
    path('new/', views.new_post, name='new_post'),
    # Профайл пользователя
    path('<int:user_id>/', views.profile, name='profile'),
    # Просмотр записи
    path('<int:user_id>/<int:post_id>/', views.post_view, name='post'),
    path(
        '<int:user_id>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit',
    ),
    path(
        '<int:user_id>/<int:post_id>/comment',
        views.add_comment, name='add_comment',
    ),
    path(
        '<int:user_id>/follow/',
        views.profile_follow,
        name='profile_follow',
    ),
    path(
        '<int:user_id>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
]
