from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import PetitionForm, CommentForm
from django.core.serializers import serialize
from rest_framework_tracking.mixins import LoggingMixin
from django.views.generic import View
from rest_framework import views
from django.db.models import Count
# from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


from functools import wraps

from django.conf import settings
from django.utils.module_loading import import_string

from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.core import is_ratelimited


ALL = (None,)


def ratelimit(group=None, key=None, rate=None, method=ALL, block=True):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(request, *args, **kw):
            old_limited = getattr(request, 'limited', False)
            ratelimited = is_ratelimited(request=request, group=group, fn=fn,
                                         key=key, rate=rate, method=method,
                                         increment=True)
            request.limited = ratelimited or old_limited
            if ratelimited and block:
                cls = getattr(
                    settings, 'RATELIMIT_EXCEPTION_CLASS', Ratelimited)
                return redirect('error_page')
            return fn(request, *args, **kw)
        return _wrapped
    return decorator


class PetitionCreateView(LoggingMixin, LoginRequiredMixin, views.APIView):
    template_name = 'main/petition_create.html'
    login_url = '/login/'  # Update with your login URL

    def get(self, request):
        form = PetitionForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(ratelimit(key='ip', rate='1/m', method='POST'), name='dispatch')
    def post(self, request):
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.user = request.user
            petition.save()
            return redirect('petition_list')
        return render(request, self.template_name, {'form': form})


class MyPetitionsView(LoggingMixin, LoginRequiredMixin, views.APIView):
    template_name = 'main/my_petitions.html'

    def get(self, request):
        user_petitions = Petition.objects.filter(user=request.user).order_by('-created')
        return render(request, self.template_name, {'user_petitions': user_petitions})


class PetitionsView(views.APIView):
    template_name = 'main/all_petitions.html'

    def get(self, request):
        query = request.GET.get('q')
        if query:
            user_petitions = Petition.objects.filter(title__icontains=query).annotate(
                like_count=Count('likes'),
                dislike_count=Count('dislikes'),
                comment_count=Count('comment')
            ).order_by('-created')
        else:
            user_petitions = Petition.objects.annotate(
                like_count=Count('likes'),
                dislike_count=Count('dislikes'),
                comment_count=Count('comment')
            ).order_by('-created')
        return render(request, self.template_name, {'user_petitions': user_petitions})


class PetitionView(LoggingMixin, views.APIView):
    template_name = 'main/petition_detail.html'

    def get(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        likes_count = Likes.objects.filter(petition=petition).count()
        dislikes_count = Dislikes.objects.filter(petition=petition).count()
        comments = Comment.objects.filter(petition=petition).order_by('-created')
        return render(request, self.template_name,
                      {'petition': petition, 'likes_count': likes_count, 'dislikes_count': dislikes_count, 'comments': comments})


class LikeView(LoggingMixin, LoginRequiredMixin, views.APIView):

    @method_decorator(ratelimit(key='ip', rate='1/m', method='POST'), name='dispatch')
    def post(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        like, created = Likes.objects.get_or_create(user=request.user, petition=petition)
        if not created:
            like.delete()
        return redirect('petition_detail', pk=pk)


class DislikeView(LoggingMixin, LoginRequiredMixin, views.APIView):

    @method_decorator(ratelimit(key='ip', rate='1/m', method='POST'), name='dispatch')
    def post(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        dislike, created = Dislikes.objects.get_or_create(user=request.user, petition=petition)
        if not created:
            dislike.delete()
        return redirect('petition_detail', pk=pk)


# @ratelimit(key='ip', rate='5/m')
class CommentCreateView(LoggingMixin, LoginRequiredMixin, views.APIView):

    @method_decorator(ratelimit(key='ip', rate='1/m', method='POST'), name='dispatch')
    def post(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        comment_form = CommentForm(request.POST)  # Create an instance of CommentForm with form data
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']  # Get the 'text' field value from the form
            Comment.objects.create(user=request.user, petition=petition, text=text)
            return redirect('petition_detail', pk=pk)
        else:
            # If form data is invalid, render the form again with error messages
            return render(request, 'main/petition_detail.html', {'petition': petition, 'comment_form': comment_form})