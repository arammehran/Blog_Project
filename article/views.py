from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm
from user.models import User
from .models import Article, CommentCount, Notifications, Comment
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponseForbidden


class ArticleListView(ListView):
    model = Article
    template_name = 'home.html'
    context_object_name = 'articles'
    ordering = ['-created_at']


class NotificationsView(View):
    template_name = 'notifications.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.role == 'r':
            notification_obj = current_user.receiver.order_by("-created_at").all()
            context = {'notifications': notification_obj}
            return render(request, self.template_name, context)


class NotificationReadView(View):
    def post(self, request, *args, **kwargs):
        current_user = request.user
        current_user.receiver.all().update(is_read=True)
        return redirect('notifications')


class LikedArticleView(ListView):
    model = Article
    template_name = 'liked_articles.html'


class LikeView(View):
    def post(self, request, article_id, like):
        article_obj = Article.objects.get(id=article_id)
        if like:
            article_obj.likes.add(request.user)
            article_obj.like_count += 1
        else:
            article_obj.likes.remove(request.user)
            article_obj.like_count -= 1
        article_obj.save()
        return redirect('home')


def increment_count(a, b):
    obj, created = CommentCount.objects.get_or_create(reader=a, article=b)
    if created:
        return None
    else:
        obj.comment_count += 1
        obj.save()
        return None


class ArticleCreateView(View):
    form_class = ArticleForm
    template_name = 'article_create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.role != 'a':
            return HttpResponseForbidden()
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = user
            obj.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class ArticleUpdateView(View):
    template_name = 'article_update.html'

    def get(self, request, article_id):
        obj = Article.objects.get(id=article_id)
        if obj.author == request.user:
            form = ArticleForm(instance=obj)
            context = {'article': obj, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, article_id):
        obj = Article.objects.get(id=article_id)
        if obj.author == request.user:
            form = ArticleForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('home')
            context = {'article': obj, 'form': form}
        return render(request, self.template_name, context)


class CommentCreateView(View):
    form_class = CommentForm
    template_name = 'comment_create.html'

    def get(self, request, article_id):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, article_id):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            article_obj = Article.objects.get(id=article_id)
            obj.reader = user
            obj.articles = article_obj
            increment_count(a=user, b=article_obj)
            comment_obj = CommentCount.objects.filter(reader=user, article=article_obj).first()
            if user.role == 'r' and comment_obj.comment_count < 3:
                obj.save()
                return redirect('home')
            else:
                return HttpResponseForbidden()
        return render(request, self.template_name, {'form': form})


class CommentUpdateView(View):
    template_name = 'comment_update.html'

    def get(self, request, comment_id):
        obj = Comment.objects.get(id=comment_id)
        if obj.reader == request.user:
            form = CommentForm(instance=obj)
        return render(request, self.template_name, {'form': form})

    def post(self, request, comment_id):
        obj = Comment.objects.get(id=comment_id)
        if obj.reader == request.user:
            form = CommentForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('home')
        return render(request, self.template_name, {'form': form})
