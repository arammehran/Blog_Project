from django.shortcuts import render, redirect, Http404
from django.views import View
from .models import User, Followers
from .forms import UserRegistrationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from article.models import Comment


class FollowedAuthorsView(View):
    template_name = 'followed_authors.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class AuthorProfileView(View):
    template_name = 'author_profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            author_obj = User.objects.get(id=kwargs.get('id'))
            follower_obj, created = Followers.objects.get_or_create(author=author_obj)
            context = {
                'author': author_obj,
                'follower': follower_obj,
            }
            return render(request, self.template_name, context)
        else:
            return redirect('home')


class FollowAuthorView(View):
    def post(self, request, follow, *args, **kwargs):
        user = request.user
        author_obj = User.objects.get(id=kwargs.get('id'))
        follower_obj = Followers.objects.get(author=author_obj)
        if follow:
            follower_obj.reader.add(user)
        else:
            follower_obj.reader.remove(user)
        return redirect('home')


class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_pass')
