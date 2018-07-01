from django.test import TestCase
from core.models import UserProfile
from django.contrib.auth import get_user_model
from model_mommy import mommy
from core.pipeline import save_profile
from social_core.backends.github import GithubOAuth2
from rest_framework.response import Response

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = mommy.make(get_user_model())

    def test_save_profile(self):
        backend = GithubOAuth2()
        response = Response()
        save_profile(backend, self.user, response, True)
        with self.assertRaises(get_user_model().userprofile.RelatedObjectDoesNotExist):
            self.user.userprofile
        save_profile(backend, self.user, response, False)
        with self.assertRaises(get_user_model().userprofile.RelatedObjectDoesNotExist):
            self.user.userprofile

        response['name'] = 'Tiago Costa'
        response['login'] = 'tcostam'
        response['avatar_url'] = 'https://avatars1.githubusercontent.com/u/3596239?s=460&v=4'
        response['html_url'] = 'https://github.com/tcostam'
        save_profile(backend, self.user, response, False)
        with self.assertRaises(get_user_model().userprofile.RelatedObjectDoesNotExist):
            self.user.userprofile

        save_profile(backend, self.user, response, True)
        self.assertIsNotNone(self.user.userprofile)

