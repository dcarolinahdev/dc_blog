import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Post

# Tests for model Post
class PostModelTests(TestCase):
    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently() returns False for posts whose published_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(published_date=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_was_published_recently_with_old_post(self):
        """
        was_published_recently() returns False for posts whose published_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_post = Post(published_date=time)
        self.assertIs(old_post.was_published_recently(), False)


    def test_was_published_recently_with_recent_post(self):
        """
        was_published_recently() returns True for posts whose published_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_post = Post(published_date=time)
        self.assertIs(recent_post.was_published_recently(), True)
