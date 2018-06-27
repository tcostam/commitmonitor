from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserProfileSerializer, RepositorySerializer, CommitSerializer
from .models import UserProfile, Repository, Commit
from rest_framework.exceptions import PermissionDenied
from rest_framework_extensions.mixins import NestedViewSetMixin
from .services import *

# ViewSets
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RepositoryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def commits(self, request, pk=None):
        queryset = Repository.objects.all()
        repository = get_object_or_404(queryset, pk=pk, user_profile=request.user.userprofile)
        commits = repository.commits
        serializer = CommitSerializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request):
        queryset = request.user.userprofile.repositories
        serializer = RepositorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Repository.objects.all()
        repository = get_object_or_404(queryset, pk=pk, user_profile=request.user.userprofile)
        serializer = RepositorySerializer(repository)
        return Response(serializer.data)

    def create(self, request):
        repository = create_repository(user_profile=request.user.userprofile,
                            name=request._data['name'],
                            access_token=request.user.social_auth.get(provider='github').extra_data['access_token'])
        serializer = RepositorySerializer(repository)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

class CommitViewSet(viewsets.ModelViewSet):
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer

    def list(self, request):
        queryset = Commit.objects.filter(repository__user_profile=request.user.userprofile).order_by('-date')

        repository_name = self.request.query_params.get('repository', None)
        if repository_name is not None:
            queryset = queryset.filter(repository__name=repository_name)
        serializer = CommitSerializer(queryset, many=True)
        return Response(serializer.data)

@login_required
def home(request):
    context = {
        'avatar':request.user.userprofile.github_avatar_url,
        'login':request.user.userprofile.github_login,
    }
    return render(request, 'core/home.html', context)


