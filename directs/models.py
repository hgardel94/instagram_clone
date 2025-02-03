# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        ordering = ['-updated_at']  

    def __str__(self):
        return f"Conversación {self.id}"
    
    

class Message(models.Model):
    conversation = models.ForeignKey( Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey( User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.JSONField(default=dict, blank = True)  

    def mark_as_read(self, user):
        self.read_by[str(user.id)] = timezone.now().isoformat()
        self.save()

    def is_unread_by(self, user):
        return str(user.id) not in self.read_by
    
    def is_read_by(self, user):
        return str(user.id) in self.read_by

    class Meta:
        ordering = ['timestamp']