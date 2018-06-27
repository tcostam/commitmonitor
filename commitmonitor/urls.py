from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from core import views as core_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from rest_framework import routers
from core import views as api_views


import django_js_reverse.views


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),
    # url(r'^$', TemplateView.as_view(template_name='exampleapp/home.html'), name='home'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Routers
router = routers.DefaultRouter()
router.register(r'userprofiles', api_views.UserProfileViewSet)
router.register(r'repositories', api_views.RepositoryViewSet)
router.register(r'commits', api_views.CommitViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + urlpatterns
