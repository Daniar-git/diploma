# your_app/forms.py
from django import forms
from .models import Petition, Likes, Dislikes, Comment


class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description']


class LikesForm(forms.ModelForm):
    class Meta:
        model = Likes
        fields = []


class DislikesForm(forms.ModelForm):
    class Meta:
        model = Dislikes
        fields = []


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
