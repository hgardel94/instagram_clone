from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from PIL import Image, ImageFilter
from accounts.models import Profile
# Create your models here.



@deconstructible
class PathAndRename:
    def __init__(self, subfolder):
        self.subfolder = subfolder

    def __call__(self, instance, filename):
        return f"images/{instance.user.username}/posts/{filename}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True)
    image = models.ImageField(upload_to=PathAndRename('posts/'), null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    quote = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.quote
    

    
    def total_likes(self):
        return self.likes.count()
    
    def liked_by_user(self, user):
        return self.likes.filter(user=user).exists()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 500 or img.width > 600:
                output_size = (500, 550)
                img = img.resize(output_size, Image.LANCZOS)  
                img.save(self.image.path)
    
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
        
        





