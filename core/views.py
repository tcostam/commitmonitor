import hmac
from hashlib import sha1

from django.conf import settings
from django.utils.encoding import force_bytes
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .serializers import UserProfileSerializer, RepositorySerializer, CommitSerializer
from .models import UserProfile, Repository, Commit
from .services import create_repository


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

@require_POST
@csrf_exempt
def hook(request):
    # Verify the request signature
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if header_signature is None:
        return HttpResponseForbidden('Permission denied.')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return HttpResponseServerError('Operation not supported.', status=501)

    mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha1)
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden('Permission denied.')

    # Process GitHub events
    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

    if event == 'ping':
        return HttpResponse('pong')
    elif event == 'push':
        # XXX TODO
        print(">>>>>>>")
        print(request.__dict__)

        return HttpResponse('success')

    # neither a ping or push
    return HttpResponse(status=204)
