from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeFeedView.as_view(), name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add_news/', add_news, name='add_news'),
    path('edit_news/<int:news_id>', UpdateNewsView.as_view(), name='edit_news'),
    path('delete_news/<int:news_id>', DeleteNewsView.as_view(), name='delete_news'),
    path('personal_page/<int:author_id>', AuthorPageView.as_view(), name='author_page'),
    path('subscribe/<int:author_id>', subscribe, name='subscribe')
]
