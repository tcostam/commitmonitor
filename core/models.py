from __future__ import unicode_literals

from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    github_login = models.CharField(max_length=255, blank=True)
    github_avatar_url = models.CharField(max_length=255, blank=True)
    github_html_url = models.CharField(max_length=255, blank=True)
