import hmac
import json
from hashlib import sha1

from django.conf import settings
from django.utils.encoding import force_bytes
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .serializers import UserProfileSerializer, RepositorySerializer, CommitSerializer
from .models import UserProfile, Repository, Commit
from .services import CreateRepositoryService, PaginationService


# ViewSets
class RepositoryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def create(self, request):
        github_token = request.user.social_auth.get(provider='github').extra_data['access_token']
        service = CreateRepositoryService(user_profile_id=request.user.userprofile.id,
                            github_token=github_token)
        service.create_webhook(name=request._data['name'])
        repository = service.create_repository(name=request._data['name'])

        serializer = RepositorySerializer(repository)
        return Response(serializer.data)

class CommitViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer

    def list(self, request):
        queryset = Commit.objects.filter(repository__user_profile=request.user.userprofile).order_by('-date')

        repository_name = self.request.query_params.get('repository', None)
        if repository_name is not None:
            queryset = queryset.filter(repository__name=repository_name)

        current_page = request.META.get('HTTP_X_CURRENT_PAGE', 0)
        per_page = request.META.get('HTTP_X_PER_PAGE', 10)

        pagination = PaginationService(items=queryset, current_page=current_page, per_page=per_page)
        paginated_items = pagination.page_items

        serializer = CommitSerializer(paginated_items, many=True)
        return Response(serializer.data, headers=pagination.header_params)

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
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        commits = body['commits']
        repository_full_name = body['repository']['full_name']

        queryset = Repository.objects.all()
        repository = get_object_or_404(queryset, full_name=repository_full_name)

        for commit in commits:
            Commit.objects.create(repository=repository,
                                    github_html_url=str(commit['url'] or ''),
                                    sha=commit['id'],
                                    github_author_name=str(commit['author']['name'] or ''),
                                    message=str(commit['message'] or ''),
                                    date=commit['timestamp'])

        return HttpResponse('success')

    # Neither a ping or push
    return HttpResponse(status=204)
