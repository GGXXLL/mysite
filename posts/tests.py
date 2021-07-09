import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post, Part, Examine


class PostModelTests(TestCase):

    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(pub_date=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_was_published_recently_with_old_post(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        future_post = Post(pub_date=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_was_published_recently_with_recent_post(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() - datetime.timedelta(hours=23)
        future_post = Post(pub_date=time)
        self.assertIs(future_post.was_published_recently(), True)


class PostIndexViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test", password="test")
        cls.part = Part.objects.create(name='python')

    def test_no_post(self):
        resp = self.client.get(reverse("posts:posts"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "暂无博客，敬请期待")
        self.assertQuerysetEqual(resp.context['post_list'], [])

    def test_query_part_post(self):
        post = Post.objects.create(title="test", text="test", part=self.part, author=self.user, examine=Examine.PASS)
        url = reverse("posts:posts") + f"?part={post.part_id}"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(resp.context['post_list'], [post])

    def test_query_search_post(self):
        post = Post.objects.create(title="test", text="test", part=self.part, author=self.user, examine=Examine.PASS)
        url = reverse("posts:posts") + f"?q={post.text}"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(resp.context['post_list'], [post])
