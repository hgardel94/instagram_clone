from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<str:pk>/', views.edit_post, name='edit_post'),
    path('delete_post/<str:pk>/', views.delete_post, name='delete_post')
    
]