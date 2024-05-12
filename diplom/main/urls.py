from django.urls import path
from .views import *

urlpatterns = [
    path("petitions/all/", PetitionsView.as_view(), name="petitions"),
    path("petitions/create/", PetitionCreateView.as_view(), name='petition_create'),
    path("petitions/my/", MyPetitionsView.as_view(), name='petition_list'),
    path("petitions/<int:pk>", PetitionView.as_view(), name='petition_detail'),
    path("petition/comment/<int:pk>/", CommentCreateView.as_view(), name='comment_create'),
    path('main/petition/like/<int:pk>/', LikeView.as_view(), name='like_petition'),
    path("petition/dislike/<int:pk>/", DislikeView.as_view(), name='dislike_petition'),
    # path("petitions/closed/", ),
]


