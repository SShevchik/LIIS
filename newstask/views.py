from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import News, Subscription
from .forms import UserRegisterForm, UserLoginForm, NewsForm
from .utils import group_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('author'):
                user.groups.add(Group.objects.get(name='author'))
            else:
                user.groups.add(Group.objects.get(name='subscriber'))
            login(request, user)
            messages.success(request, 'You have successfully registered')
            return redirect('home')
        else:
            messages.error(request, 'Registration error')
    else:
        form = UserRegisterForm()
    return render(request, 'form.html', context={'form': form, 'title': 'Register page', 'namepage': 'Register',
                                                 'buttontext': 'Create account'})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'form.html',
                  context={'form': form, 'title': 'Log in page', 'namepage': 'Log in', 'buttontext': 'Log in'})


def user_logout(request):
    logout(request)
    return redirect('home')


class HomeFeedView(ListView):
    model = News
    template_name = 'newstask/index.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home page'
        context['header'] = 'Feed list'
        return context

    def detect_user_group(self):
        user_groups = []
        for group in self.request.user.groups.values_list('name', flat=True):
            user_groups.append(group)
        return user_groups

    def get_queryset(self):
        user_groups = self.detect_user_group()
        if ('subscriber' in user_groups) or ('author' in user_groups):
            authors = list(Subscription.objects.filter(subscriber_id=self.request.user.id).values('author'))
            if authors:
                return News.objects.filter(Q(author_id=self.request.user) | Q(access_category__in=['PC', 'AD']) | Q(
                    author_id__in=authors[0].values()))
            else:
                return News.objects.filter(Q(author_id=self.request.user) | Q(access_category__in=['PC', 'AD']))
        else:
            return News.objects.filter(access_category='PC')


@group_required('author')
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            new_news = form.save(commit=False)
            new_news.author = request.user
            new_news.save()
            messages.success(request, 'News successfully created')
        return redirect('author_page', author_id=request.user.id)
    else:
        form = NewsForm()
    return render(request, 'form.html',
                  context={'form': form, 'title': 'Add news', 'namepage': 'Add news', 'buttontext': 'Create'})


class UpdateNewsView(UserPassesTestMixin, UpdateView):
    group_required = ['author']
    model = News
    template_name = 'form.html'
    pk_url_kwarg = 'news_id'
    form_class = NewsForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_id'] = self.pk_url_kwarg
        context['title'] = 'Edit'
        context['namepage'] = 'Edit news'
        context['buttontext'] = 'Save'
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class DeleteNewsView(UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'newstask/delete_news.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'news_id'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class AuthorPageView(ListView):
    model = News
    template_name = 'newstask/author_page.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Personal author page'
        author = User.objects.get(id=self.kwargs['author_id'])
        context['author'] = author
        return context

    def get_queryset(self):
        if self.kwargs['author_id'] == self.request.user.id:
            return News.objects.filter(author_id=self.kwargs['author_id'])
        if Subscription.objects.filter(Q(subscriber_id=self.request.user.id) & Q(author_id=self.kwargs['author_id'])):
            return News.objects.filter(author_id=self.kwargs['author_id'])
        elif self.request.user.id:
            return News.objects.filter(Q(access_category__in=['PC', 'AD']) & Q(author_id=self.kwargs['author_id']))
        return News.objects.filter(Q(access_category='PC') & Q(author_id=self.kwargs['author_id']))


def subscribe(request, author_id):
    if request.method == 'GET':
        try:
            subscriber = User.objects.get(id=request.user.id)
        except:
            raise PermissionDenied
        author = User.objects.get(id=author_id)
        if author.groups.filter(name='author').exists() and request.user.id != author_id:
            if not (Subscription.objects.filter(Q(author=author_id) & Q(subscriber=request.user.id))):
                record = Subscription(author=author, subscriber=subscriber)
                record.save()
                messages.success(request, 'You have successfully subscribed')
                return redirect('author_page', author_id=author_id)
            else:
                messages.error(request, 'You are already subscribed')
        else:
            messages.error(request, 'You are trying to follow a non-author user')
    return render(request, 'newstask/index.html')
