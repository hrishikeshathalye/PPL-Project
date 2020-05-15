from django.urls import path
from .views import PostListViewGenUser, PostListViewVolunteer, PostDetailView, PostCreateView, PostUpdateView, PostDeleteViewGenUser, PostDeleteViewVolunteer, UserPostListView, UsersDisplayView
from . import views

urlpatterns = [
    path('', views.logout_home, name='logout-home'),
    path('home/volunteer/', PostListViewVolunteer.as_view(), name='home-volunteer'),
    path('home/genuser/', PostListViewGenUser.as_view(), name='home-genuser'),
    path('users/', UsersDisplayView.as_view(), name='users-view'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post-genuser/<int:pk>/delete', PostDeleteViewGenUser.as_view(), name='post-delete-genuser'),
    path('post-volunteer/<int:pk>/delete', PostDeleteViewVolunteer.as_view(), name='post-delete-volunteer'),
    path('notfriend/', views.not_friend, name='not-friend'),
    path('about/', views.about, name='blog-about'),
    path('report/', views.report_post, name='report_post'),
    path('like/', views.like_post, name='like_post'),
    path('dislike/', views.dislike_post, name='dislike_post'),
    path('liked_posts/', views.liked_posts, name='liked-posts'),
    path('connect/<str:operation>/<int:pk>/', views.change_friends, name='change_friends'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
]