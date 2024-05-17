from django.urls import path, include

from diplom.user.views import profile, error_page

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('error/', error_page, name="error_page"),
]
