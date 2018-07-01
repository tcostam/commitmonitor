from .models import UserProfile


def save_profile(backend, user, response, is_new, *args, **kwargs):
    if backend.name == 'github' and is_new and ('name' in response) and ('login' in response):
        name = response['name']
        github_login = response['login']
        github_avatar_url = response['avatar_url'] or ''
        github_html_url = response['html_url'] or ''

        UserProfile.objects.create(
            user=user, name=name, github_login=github_login,
            github_avatar_url=github_avatar_url,
            github_html_url=github_html_url)
