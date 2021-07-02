import datetime

from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Examine(models.IntegerChoices):
    WAITING = 1
    PASS = 2
    REJECT = 3


class Part(models.Model):
    name = models.CharField(max_length=20, verbose_name='版块')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "版块"
        verbose_name_plural = "版块"


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题', null=False)
    text = models.TextField(verbose_name='正文', null=False)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, verbose_name='所属版块', null=False)
    agree_count = models.IntegerField(verbose_name='赞同量', default=0)
    disagree_count = models.IntegerField(verbose_name='反对量', default=0)
    views_count = models.IntegerField(verbose_name='浏览量', default=0)
    comments_count = models.IntegerField(verbose_name='评论数', default=0)
    pub_date = models.DateTimeField(verbose_name='发布日期', default=timezone.now)
    edit_date = models.DateTimeField(verbose_name='编辑日期', default=timezone.now)
    examine = models.IntegerField(verbose_name='审核状态', default=1, choices=Examine.choices)
    is_delete = models.BooleanField(verbose_name='被删除？', default=False)

    def __str__(self):
        return self.title

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='最近发布?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        verbose_name = "帖子"
        verbose_name_plural = "帖子"

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='帖子', null=False)
    text = models.CharField(max_length=200, verbose_name='内容', null=False)
    sub = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='子评论', null=True)
    agree = models.IntegerField(default=0, verbose_name='赞同')
    disagree = models.IntegerField(default=0, verbose_name='反对')
    examine = models.IntegerField(verbose_name='审核状态', default=1, choices=Examine.choices)
    is_delete = models.BooleanField(verbose_name='被删除？', default=False)
    pub_date = models.DateTimeField(verbose_name='发布日期', default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
