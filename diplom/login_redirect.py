# myapp/middleware.py
from django.shortcuts import redirect

class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'next' in request.GET:
            return redirect("https://diplom.aitu.lol/")
        return response
