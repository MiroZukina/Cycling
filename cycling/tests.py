import unittest
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from cycling.models import Post, Comment, Profile, City, create_profile
from django.db.models.signals import post_save
from django.utils import timezone
from cycling.views import home, profile_list
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test-user', password='test-12345')
        self.post = Post.objects.create(user=self.user, body='Test Body', post_image_url='http://example.com', created_at=timezone.now())

    def test_number_of_likes(self):
        self.assertEqual(self.post.number_of_likes(), 0)  

    def test_str_representation(self):
        expected_str = f"{self.user}({self.post.created_at:%Y-%m-%d %H:%M}):Test Body..."
        self.assertEqual(str(self.post), expected_str)

if __name__ == '__main__':
    unittest.main()


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test-user', password='test12344')
        self.post = Post.objects.create(user=self.user, body='Test Post Body', post_image_url='http://example.com', created_at=timezone.now())
        self.comment = Comment.objects.create(user=self.user, post=self.post, text='Test Comment Text', created_at=timezone.now())

    def test_comment_str_representation(self):
        expected_str = f"{self.user} on {self.post} at {self.comment.created_at:%Y-%m-%d %H:%M}"
        self.assertEqual(str(self.comment), expected_str)

    def test_comment_user_relationship(self):
        self.assertEqual(self.comment.user, self.user)

class ProfileModelTestCase(TestCase):
    def test_profile_creation(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
        self.assertIsNotNone(profile.date_modified)
        self.assertEqual(profile.follows.count(), 1)  

    def test_create_profile_signal_handler(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        self.assertTrue(Profile.objects.filter(user=user).exists())
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.follows.count(), 1)  

if __name__ == '__main__':
    unittest.main()

class CityModelTestCase(TestCase):
    def test_city_creation(self):
        city = City.objects.create(name='Test City')
        saved_city = City.objects.get(name='Test City')
        self.assertEqual(saved_city.name, 'Test City')

    def test_city_str_representation(self):
        city = City.objects.create(name='Test City')
        self.assertEqual(str(city), 'Test City')

    def test_verbose_name_plural(self):
        verbose_name_plural = City._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'cities')



if __name__ == '__main__':
    unittest.main()


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test-user', password='test1234')
        self.post = Post.objects.create(user=self.user, body='Test Post Body')
        self.comment = Comment.objects.create(user=self.user, post=self.post, text='Test Comment Text')

    def test_home_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue('posts' in response.context)
        self.assertTrue('form' in response.context)
        self.assertTrue('comments' in response.context)
        self.assertTrue('comment_form' in response.context)

    def test_home_view_post(self):
        self.client.force_login(self.user)
        data = {'text': 'Test Comment Text'}
        response = self.client.post(reverse('home'), data)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Comment.objects.count(), 2)  

if __name__ == '__main__':
    unittest.main()

    class ProfileListViewTestCase(TestCase):
        def setUp(self):
            self.factory = RequestFactory()
            self.user = User.objects.create_user(username='test-user', password='test1234')
            if not hasattr(self.user, 'profile'):
                self.profile = Profile.objects.create(user=self.user)

        def test_authenticated_user_profile_list(self):
            request = self.factory.get(reverse('profile_list'))
            request.user = self.user

            # Required to test messages in the view
            setattr(request, 'session', 'session')
            messages = FallbackStorage(request)
            setattr(request, '_messages', messages)

            response = profile_list(request)
            self.assertEqual(response.status_code, 200)
            self.assertTrue('profiles' in response.context)
            if hasattr(self.user, 'profile'):
                self.assertNotIn(self.user.profile, response.context['profiles'])

        def test_unauthenticated_user_profile_list(self):
            request = self.factory.get(reverse('profile_list'))
            request.user = User.objects.create_user(username='unauthenticated_user', password='password123')

            response = profile_list(request)
            self.assertEqual(response.status_code, 302)  # Redirect expected for unauthenticated user

    if __name__ == '__main__':
        unittest.main()