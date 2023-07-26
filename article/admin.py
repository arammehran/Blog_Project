from django.contrib import admin
from .models import Article, Comment, CommentCount, Notifications

models_list = [Article, Comment, CommentCount, Notifications]
admin.site.register(models_list)
