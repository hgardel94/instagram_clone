from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<str:pk>/', views.edit_post, name='edit_post'),
    path('delete_post/<str:pk>/', views.delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('remove_like_post/<int:post_id>/', views.remove_like_post, name='remove_like_post'),
    path('comments/<int:post_id>/', views.load_comments, name='load_comments'),
    path('post/<int:post_id>/', views.post_comment, name='post_comment'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)