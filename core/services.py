from github import Github, GithubException, UnknownObjectException
from .models import UserProfile, Repository, Commit
from rest_framework.exceptions import NotFound, ValidationError
from django.conf import settings
import datetime
import math


class PaginationService:
    def __init__(self, items, current_page=0, per_page=20):
        self.__items = items
        self.__per_page = int(per_page)
        self.__current_page = int(current_page)
        self.__pages_count = math.ceil(items.count() / float(per_page))

    @property
    def page_items(self):
        offset = self.__current_page * self.__per_page
        limit = offset + self.__per_page
        return self.__items[offset:limit]

    @property
    def header_params(self):
        return { 'Pages-Count': self.__pages_count, 'Per-Page': self.__per_page, 'Current-Page': self.__current_page, 'Items-Count': self.__items.count() }

class CreateRepositoryService:
    def __init__(self, user_profile_id, github_token):
        self.__github_token = github_token
        self.__github = Github(self.__github_token)
        self.__user_profile_id = user_profile_id
        self.__user_profile = UserProfile.objects.get(pk=self.__user_profile_id)

    def create_repository(self, name):
        try:
            if Repository.objects.filter(name=name, user_profile=self.__user_profile).count() > 0:
                raise ValidationError("Repository already added.")

            repo = self.__github.get_user().get_repo(name)
            repository = Repository.objects.create(user_profile=self.__user_profile,
                                                    name=str(repo.name or ''),
                                                    full_name=str(repo.full_name or ''),
                                                    description=str(repo.description or ''),
                                                    github_html_url=str(repo.html_url or ''),
                                                    owner_github_login=str(repo.owner.login or ''),
                                                    owner_avatar_url=str(repo.owner.avatar_url or ''))

            delta = datetime.timedelta(days=30)
            one_month_ago = datetime.datetime.today() - delta
            commits = repo.get_commits(since=one_month_ago)
            for commit in commits:
                Commit.objects.create(repository=repository,
                                        github_html_url=str(commit.html_url or ''),
                                        sha=commit.sha,
                                        github_author_name=str(commit.commit.author.name or ''),
                                        message=str(commit.commit.message or ''),
                                        date=commit.commit.author.date)

            return repository
        except UnknownObjectException:
            raise NotFound("Repository not found.")

    def create_webhook(self, name):
        try:
            hook_configs = {}
            hook_configs['url'] = settings.APP_BASE_URL + '/hooks/'
            hook_configs['content_type'] = 'json'
            hook_configs['secret'] = settings.GITHUB_WEBHOOK_KEY

            repo = self.__github.get_user().get_repo(name)
            repo.create_hook(name="web", config=hook_configs, events=["push"], active=True)
        except GithubException as ex:
            # Validate if hook already exists:
            for error in ex.data['errors']:
                if error['message'] == 'Hook already exists on this repository':
                    return
            raise NotFound("Could not create webhook.")


