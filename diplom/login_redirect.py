from django.shortcuts import redirect
from django.urls import reverse


class CustomRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.path == reverse('login:index'):
                return redirect('https://diplom.aitu.lol')

        return response