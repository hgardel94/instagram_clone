from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'accounts'
urlpatterns = [
    path('', views.login_user, name='login'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('search_people/', views.search_people, name='search_people'),
    path('follow_user/<int:user_id>/', views.follow_user, name='follow_user'),
    path('profile/', views.display_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_profile_photo/', views.update_profile_photo, name='update_profile_photo'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)