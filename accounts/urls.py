from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.login_user, name='login'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('search_people/', views.search_people, name='search_people'),
    path('follow_user/<int:user_id>/', views.follow_user, name='follow_user'),
    path('profile/', views.display_profile, name='profile'),
    
]