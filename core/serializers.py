from rest_framework import serializers
from .models import UserProfile, Repository


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Repository
        fields = ('id', 'name', 'full_name')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    repositories = RepositorySerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('name', 'github_avatar_url', 'github_login', 'github_html_url', 'repositories')
