from django.test import TestCase
from model_mommy import mommy
from core.models import UserProfile, Commit
from django.urls import reverse
from django.test import Client


class CommitViewSetTestCase(TestCase):
    def setUp(self):
        mommy.make(Commit)
        self.client = Client()

    def test_user_profile_list_view(self):
        url = reverse("commit-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
