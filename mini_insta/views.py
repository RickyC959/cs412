# File: mini_insta/views.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: all the views that are part of this app
from typing import Any

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

class ShowFollowersDetailView(DetailView):
    model=Profile
    template_name= 'mini_insta/show_followers.html'
    context_object_name='followers'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile= Profile.objects.get(pk=pk)
        context["follower"] = profile.get_followers()
        return context
    

class ShowFollowingDetailView(DetailView):
    model=Profile
    template_name= 'mini_insta/show_following.html'
    context_object_name='following'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile= Profile.objects.get(pk=pk)

        context["following"] = profile.get_following()
        return context

class ShowFeedView(DetailView):
    model=Profile
    template_name='mini_insta/show_feed.html'
    context_object_name='profile'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context["feed"] = profile.get_post_feed()
        return context
class SearchView(ListView):
    template_name='mini_insta/search_results.html'

    def dispatch(self, request, *args, **kwargs):
        if 'query' not in self.request.GET:
            pk = self.kwargs['pk']
            profile = Profile.objects.get(pk = pk)
            return render(request, 'mini_insta/search.html', {'profile': profile})
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        
        query = self.request.GET.get('query')
        if query:
            return Post.objects.filter(caption__icontains=query)
        
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')

        pk = self.kwargs["pk"]
        context["profile"] = Profile.objects.get(pk=pk)
        context["query"] = query
        context['posts'] = self.get_queryset()

        if query:
            user = Profile.objects.filter(username__icontains=query)
            name = Profile.objects.filter(display_name__icontains=query)
            bio  = Profile.objects.filter(bio_text__icontains=query)

            context['profiles'] = (user | name | bio).distinct()
        else:
            context['profiles'] = Profile.objects.none()
            
        return context

    

    