from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'posts', null=True )
    image = models.ImageField(null = True)
    created_at = models.DateTimeField(auto_now_add= True)
    quote = models.TextField(null=True, blank= True)
    
    def __str__(self):
        return self.quote
    
    def total_likes(self):
        return self.likes.count()
    
    def liked_by_user(self, user):
        return self.likes.filter(user=user).exists()
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'user_comments')
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name= 'comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.post.quote
    
    
    class Meta:
        unique_together = ('user', 'post')
        
        
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = ('follower', 'following')  

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"




