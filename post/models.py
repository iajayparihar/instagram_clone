from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    link = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    following = models.PositiveIntegerField(default=0)
    follows = models.ManyToManyField("self", related_name='followed_by',symmetrical=False,blank=True)
    posts = models.ManyToManyField('Post', related_name='user_posts', blank=True)

    def __str__(self):
        return f"{self.user.username} - Profile"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    
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

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True,related_name='liked_post')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.liked_post

class Friendship(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=50, default='pending') # pending acceptd rejected
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender}, {self.status}"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User,related_name='requests_sent',on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name='requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f" from user: {self.from_user}, to : {self.to_user}"

