# your_app/forms.py
from django import forms
from .models import Petition, Likes, Dislikes, Comment
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
import re
from django.core.exceptions import ValidationError


def sanitize_input(user_input):
    pattern = re.compile(r'[{}=]')

    if pattern.search(user_input):
        raise ValidationError("Input contains prohibited characters: '{', '}', '='")

    return user_input


class PetitionForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = Petition
        fields = ['title', 'description', 'captcha']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return sanitize_input(title)

    def clean_description(self):
        description = self.cleaned_data.get('description')
        return sanitize_input(description)


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

    def clean_text(self):
        text = self.cleaned_data.get('text')
        return sanitize_input(text)
