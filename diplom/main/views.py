from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import PetitionForm, LikesForm, DislikesForm, CommentForm
from .models import *


class PetitionCreateView(View):
    template_name = 'main/petition_create.html'

    def get(self, request):
        form = PetitionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.user = request.user  # Set the current user as the creator
            petition.save()
            return redirect('petition_list')  # Change 'petition_list' to your actual URL name for the list view
        return render(request, self.template_name, {'form': form})


class MyPetitionsView(View):
    template_name = 'main/my_petitions.html'

    def get(self, request):
        user_petitions = Petition.objects.filter(user=request.user).order_by('-created')
        return render(request, self.template_name, {'user_petitions': user_petitions})


class PetitionView(View):
    template_name = 'main/petition_detail.html'

    def get(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        return render(request, self.template_name, {'petition': petition})