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

        # 1. Check if there is a repository in users github
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
        # 4. Return repository or error
        return repository
    except UnknownObjectException:
        raise NotFound("Repository not found.")

