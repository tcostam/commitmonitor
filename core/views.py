from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    print(">>>>>>>>")
    print(request.user.social_auth.get(provider='github').extra_data['access_token'])
    print("<<<<<<<<")
    return render(request, 'core/home.html')
