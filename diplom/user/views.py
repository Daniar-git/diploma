from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework_tracking.mixins import LoggingMixin

@login_required
def profile(request):
    user = request.user
    return render(request, 'user/profile.html', {'user': user})


def home_page(request):
    return render(request, 'home/index.html')


def error_page(request):
    return render(request, 'home/error_page.html')