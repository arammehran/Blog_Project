from django.db import models
from user.models import BaseModel, User


class Article(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    like_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='blog_post')


class Comment(BaseModel):
    articles = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class CommentCount(BaseModel):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_count = models.IntegerField(default=0)


class Notifications(BaseModel):
    author = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    reader = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
