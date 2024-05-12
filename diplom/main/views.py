from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import PetitionForm, CommentForm
from django.core.serializers import serialize
from rest_framework_tracking.mixins import LoggingMixin
from django.views.generic import View
from rest_framework import views


class PetitionCreateView(LoggingMixin, LoginRequiredMixin, View):
    template_name = 'main/petition_create.html'
    login_url = '/login/'  # Update with your login URL

    def get(self, request):
        form = PetitionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.user = request.user
            petition.save()
            return redirect('petition_list')
        return render(request, self.template_name, {'form': form})



class MyPetitionsView(LoggingMixin, LoginRequiredMixin, View):
    template_name = 'main/my_petitions.html'

    def get(self, request):
        user_petitions = Petition.objects.filter(user=request.user).order_by('-created')
        return render(request, self.template_name, {'user_petitions': user_petitions})


class PetitionsView(LoggingMixin, views.APIView):
    template_name = 'main/all_petitions.html'

    def get(self, request):
        user_petitions = Petition.objects.all().order_by('-created')
        return render(request, self.template_name, {'user_petitions': user_petitions})


class PetitionView(LoggingMixin, View):
    template_name = 'main/petition_detail.html'

    def get(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        likes_count = Likes.objects.filter(petition=petition).count()
        dislikes_count = Dislikes.objects.filter(petition=petition).count()
        comments = Comment.objects.filter(petition=petition).order_by('-created')
        return render(request, self.template_name,
                      {'petition': petition, 'likes_count': likes_count, 'dislikes_count': dislikes_count, 'comments': comments})


class LikeView(LoggingMixin, LoginRequiredMixin, View):
    def post(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        like, created = Likes.objects.get_or_create(user=request.user, petition=petition)
        if not created:
            like.delete()
        return redirect('petition_detail', pk=pk)


class DislikeView(LoggingMixin, LoginRequiredMixin, View):
    def post(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        dislike, created = Dislikes.objects.get_or_create(user=request.user, petition=petition)
        if not created:
            dislike.delete()
        return redirect('petition_detail', pk=pk)


class CommentCreateView(LoggingMixin, LoginRequiredMixin, View):
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