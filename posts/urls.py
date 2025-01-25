from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<str:pk>/', views.edit_post, name='edit_post'),
    path('delete_post/<str:pk>/', views.delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('remove_like_post/<int:post_id>/', views.remove_like_post, name='remove_like_post'),
    path('comments/<int:post_id>/', views.load_comments, name='load_comments'),

    
]