from django.urls import path
from .views import *

urlpatterns = [
    # path("petitions/all/", ),
    path("petitions/create/", PetitionCreateView.as_view(), name='petition_create'),
    path("petitions/my/", MyPetitionsView.as_view(), name='petition_list'),
    path("petitions/<int:pk>", PetitionView.as_view(), name='petition_detail'),
    # path("petitions/closed/", ),
]


