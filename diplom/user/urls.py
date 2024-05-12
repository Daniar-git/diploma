from django.urls import path, include

from diplom.user.views import profile

urlpatterns = [
    path('profile/', profile, name="profile"),
]
