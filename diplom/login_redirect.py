from django.shortcuts import redirect
from django.urls import reverse


class CustomRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            login_url = "https://diplom.aitu.lol/login/"
            if request.path == login_url:
                next_url = request.GET.get('next', 'https://diplom.aitu.lol')
                return redirect(next_url)

        return response
