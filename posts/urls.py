# -*- encoding: utf-8 -*-
"""
@Author : rock
@Email  : gaoxiaolei@donews.com
@Time   : 2021/6/29 9:32:15
@Docs   : do something
"""
from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostIndexView.as_view(), name='posts'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.PostEditView.as_view(), name='edit'),
    path('<int:pk>/comments/', views.CommentsView.as_view(), name='comments'),
    path('parts/', views.PartView.as_view(), name='parts'),

    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
