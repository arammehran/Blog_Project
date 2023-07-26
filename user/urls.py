from django.urls import path
from .views import (logout_view, PasswordsChangeView, RegisterView, AuthorProfileView,
                    FollowAuthorView, FollowedAuthorsView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('password/', PasswordsChangeView.as_view(template_name='change_password.html'), name='password'),
    path('password-success/', PasswordsChangeView.as_view(template_name='password_success.html'), name='password_pass'),
    path('authorProfile/<uuid:id>/', AuthorProfileView.as_view(), name='author-profile'),
    path('followAuthor/<uuid:id>/<int:follow>', FollowAuthorView.as_view(), name='follow-author'),
    path('followedAuthors/', FollowedAuthorsView.as_view(), name='followed-authors'),

]
