# File: mini_insta/views.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: all the views that are part of this app
from django.shortcuts import render
from django.views.generic import *
from .models import *
from .forms import * 
from django.urls import reverse
# Create your views here.


class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = "profile"

class UpdateProfileView(UpdateView):
    model= Profile
    form_class= UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = "post"

class CreatePostView(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
    
        return reverse('show_profile', kwargs={'pk': pk})
    
    def get_context_data(self):

        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context

    def form_valid(self, form):

        print(form.cleaned_data)
        pk = self.kwargs('pk')
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        post = form.save()

        # image_url = self.request.POST['image_url']
        # if image_url:
        #     Photo.objects.create(post=post, image_url=image_url)

        files = self.request.FILES.getlist('image_uploads')

        for file in files:
            Photo.objects.create(post=post, image_file=file)

        return super().form_valid(form)

class DeletePostView(DeleteView):
    model = Post
    template_name ='mini_insta/delete_post_form.html'
    context_object_name = 'post'


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile= Profile.objects.get(pk=pk)
        context['profile']= profile

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        post= Post.objects.get(pk=pk)
        profile = post.profile

        return reverse('show_profile', kwargs={'pk': profile.pk}) 

class UpdatePostView(UpdateView):
    model=Post
    form_class = UpdatePostForm
    template_name='mini_insta/update_post_form.html'

