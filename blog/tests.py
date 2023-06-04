import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Post

# General functions
def create_post(post_text, days):
    """
    Create a post with the given `text` and published the
    given number of `days` offset to now (negative for posts published
    in the past, positive for posts that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(title=post_text, text=post_text, published_date=time)

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

# Test for Index View
class PostIndexViewTests(TestCase):
    def test_no_posts(self):
        """
        If no posts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerySetEqual(response.context["posts"], [])

    def test_past_post(self):
        """
        Posts with a published_date in the past are displayed on the
        index page.
        """
        post = create_post(post_text="Past published.", days=-30)
        response = self.client.get(reverse("blog:index"))
        self.assertQuerySetEqual(
            response.context["posts"],
            [post],
        )

    def test_future_post(self):
        """
        Posts with a published_date in the future aren't displayed on
        the index page.
        """
        create_post(post_text="Future published.", days=30)
        response = self.client.get(reverse("blog:index"))
        self.assertContains(response, "No posts are available.")
        self.assertQuerySetEqual(response.context["posts"], [])

    def test_future_post_and_past_post(self):
        """
        Even if both past and future posts exist, only past posts
        are displayed.
        """
        question = create_post(post_text="Past post.", days=-30)
        create_post(post_text="Future post.", days=30)
        response = self.client.get(reverse("blog:index"))
        self.assertQuerySetEqual(
            response.context["posts"],
            [question],
        )

    def test_two_past_posts(self):
        """
        The questions index page may display multiple posts.
        """
        post1 = create_post(post_text="Past post 1.", days=-30)
        post2 = create_post(post_text="Past post 2.", days=-5)
        response = self.client.get(reverse("blog:index"))
        self.assertQuerySetEqual(
            response.context["posts"],
            [post2, post1],
        )
