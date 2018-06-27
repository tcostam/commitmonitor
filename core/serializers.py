from rest_framework import serializers
from .models import UserProfile, Repository, Commit


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Repository
        fields = ('id', 'name')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    repositories = RepositorySerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('name', 'github_avatar_url', 'github_login', 'github_html_url', 'repositories')

class CommitSerializer(serializers.HyperlinkedModelSerializer):
    repository = RepositorySerializer(read_only=True)

    class Meta:
        model = Commit
        fields = ('id', 'sha', 'message', 'github_author_name', 'date', 'repository')
