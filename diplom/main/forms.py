# your_app/forms.py
from django import forms
from .models import Petition, Likes, Dislikes, Comment
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class PetitionForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = Petition
        fields = ['title', 'description', 'captcha']


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
        fields = ['text']  # Include 'text' field in the form
