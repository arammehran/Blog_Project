from django.urls import path
from .views import (ArticleCreateView, CommentCreateView, LikeView, NotificationsView, CommentUpdateView,
                    ArticleListView, LikedArticleView, NotificationReadView, ArticleUpdateView)

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('article/', ArticleCreateView.as_view(), name='article-create'),
    path('article/update/<uuid:article_id>', ArticleUpdateView.as_view(), name='article-update'),
    path('comment/<uuid:article_id>/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/update/<uuid:comment_id>', CommentUpdateView.as_view(), name='comment-update'),
    path('like/<uuid:article_id>/<int:like>/', LikeView.as_view(), name='like-article'),
    path('Liked-Articles/', LikedArticleView.as_view(), name='liked-articles'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('readNotifications/', NotificationReadView.as_view(), name='read-notifications'),

]