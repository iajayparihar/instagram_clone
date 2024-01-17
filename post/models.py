from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Profile"
        
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    comments = models.ManyToManyField(User, through='Comment', related_name='user_comments')

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post}"

    
    # The class Meta inside a Django model is used to provide additional options and configurations for the model. In your specific case:

    # In the case of -created_at, it means that when you retrieve instances of the Comment model from the database, they will be ordered in descending order based on the created_at field. The minus sign (-) before created_at indicates a descending order, meaning the newest comments will be returned first.
    class Meta:
        ordering = ['-created_at']
