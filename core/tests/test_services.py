from django.test import TestCase
from model_mommy import mommy
from core.models import UserProfile, Commit
from core.services import PaginationService, CreateRepositoryService
from github import GithubException


class PaginationServiceTestCase(TestCase):
    def setUp(self):
        mommy.make(Commit, _quantity=30)
        self.pagination_service = PaginationService(Commit.objects.all(), 0, 5)

    def test_page_items(self):
        self.assertEqual(self.pagination_service.page_items.count(), 5)
        self.assertEqual(self.pagination_service.page_items.count(), 5)

    def test_header_params(self):
        self.assertEqual(self.pagination_service.header_params['Pages-Count'], 6)
        self.assertEqual(self.pagination_service.header_params['Per-Page'], 5)
        self.assertEqual(self.pagination_service.header_params['Current-Page'], 0)
        self.assertEqual(self.pagination_service.header_params['Items-Count'], 30)

class CreateRepositoryServiceTestCase(TestCase):
    def setUp(self):
        self.user_profile = mommy.make(UserProfile)

    def test_create_repository(self):
        self.crete_repository_service = CreateRepositoryService(self.user_profile.id, None)
        with self.assertRaises(GithubException):
            self.crete_repository_service.create_repository('xpto')
