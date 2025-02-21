from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'directs'

from django.urls import path
from . import views

app_name = 'directs'

urlpatterns = [
   path('inbox/', views.inbox, name='inbox'),
   path('thread/<int:conversation_id>/', views.thread, name='thread'),
   path('send/<int:conversation_id>/', views.send_message, name='send_message'),
   path('check_conversation/<int:user_id>/', views.check_conversation, name='check_conversation'),
   path('load_users/', views.load_users, name='load_users'),
   path('send_message/', views.send_message, name='send_message'),
   path('create_conversation/', views.create_conversation, name='create_conversation'),
  
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)