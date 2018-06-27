from github import Github, GithubException, UnknownObjectException
from .models import UserProfile, Repository, Commit
from rest_framework.exceptions import NotFound, ValidationError
import datetime

def create_repository(user_profile, name, access_token):
    g = Github(access_token)
    try:
        # 0. Check if repository already exists.
        if Repository.objects.filter(name=name, user_profile=user_profile).count() > 0:
            raise ValidationError("Repository already added.")

        # 1. Check if there is a repository in user's github
        repo = g.get_user().get_repo(name)
        # 2. Create repository with all information gathered
        repository = Repository.objects.create(user_profile=user_profile,
                                                name=str(repo.name or ''),
                                                full_name=str(repo.full_name or ''),
                                                description=str(repo.description or ''),
                                                github_html_url=str(repo.html_url or ''),
                                                owner_github_login=str(repo.owner.login or ''),
                                                owner_avatar_url=str(repo.owner.avatar_url or ''))
        # 3. Get last 30 days commits
        # XXX TODO: Move to a Celery task and retry on each commit create?
        # XXX Maybe it won't be needed as we make a single request to gh.
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

        # 4. Create webhook
        # hook_configs = { url: '', content_type: 'json', secret: '' }
        # repo.create_hook(name="commitmonitor hook", config=hook_configs, events=["push"], active=True)
        # 5. Return repository
        return repository
    except UnknownObjectException:
        raise NotFound("Repository not found.")


