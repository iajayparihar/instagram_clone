from django.db import models
from django.contrib.auth.models import User

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

    class Meta:
        ordering = ['-created_at']
