# -*- encoding: utf-8 -*-
"""
@Author : rock
@Email  : gaoxiaolei@donews.com
@Time   : 2021/6/29 9:32:15
@Docs   : do something
"""
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('create/', views.Register.as_view(), name='register'),
]
