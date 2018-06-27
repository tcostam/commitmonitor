from __future__ import unicode_literals

from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    github_login = models.CharField(max_length=255, blank=True)
    github_avatar_url = models.CharField(max_length=255, blank=True)
    github_html_url = models.CharField(max_length=255, blank=True)


class Repository(models.Model):
    user_profile = models.ForeignKey('UserProfile', related_name='repositories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    github_html_url = models.CharField(max_length=255, blank=True)
    owner_github_login = models.CharField(max_length=255, blank=True)
    owner_avatar_url = models.CharField(max_length=255, blank=True)

class Commit(models.Model):
    repository = models.ForeignKey('Repository', related_name='commits', on_delete=models.CASCADE)
    github_html_url = models.CharField(max_length=255, blank=True)
    sha = models.CharField(max_length=255, blank=True)
    github_author_name = models.CharField(max_length=255, blank=True)
    message = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField()

