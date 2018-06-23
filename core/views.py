from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserProfileSerializer, RepositorySerializer
from .models import UserProfile, Repository
from rest_framework.exceptions import PermissionDenied


# ViewSets
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

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
        # 1. Check if there is a repository in users github
        # 2. Create repository with all information gathered
        # 3. Get last 30 days commits
        # 4. Return repository or error
        repository = Repository.objects.create(user_profile=request.user.userprofile, name=request._data['name'])
        serializer = RepositorySerializer(repository)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

@login_required
def home(request):
    # print(request.user.social_auth.get(provider='github').extra_data)

    context = {
        'avatar':request.user.userprofile.github_avatar_url
    }
    return render(request, 'core/home.html', context)


