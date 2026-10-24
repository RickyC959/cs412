# File: mini_insta/views.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: all the views that are part of this app
from typing import Any

from django.shortcuts import redirect, render
from django.views.generic import *
from .models import *
from .forms import * 
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
# Create your views here.


class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = "profile"
    
    def get_object(self):
        if 'pk' in self.kwargs:
            return Profile.objects.get(pk=self.kwargs['pk'])
        return Profile.objects.get(user = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_profile = self.get_object()
        
        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.filter(user=self.request.user).first()
            if logged_in_profile:
                context['is_following'] = Follower.objects.filter(
                    profile=target_profile,
                    follower_profile=logged_in_profile
                ).exists()
        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model= Profile
    form_class= UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_login_url(self):
        return reverse('login')
    
    def get_object(self):
        user = Profile.objects.get(user = self.request.user)
        return user


class PostDetailView(DetailView):
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = "post"

    def get_object(self):
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.filter(user=self.request.user).first()
            if logged_in_profile:
                context['is_liked'] = Like.objects.filter(
                    post=post,
                    profile=logged_in_profile
                ).exists()
        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    def get_context_data(self):
        context = super().get_context_data()
        
        profile = Profile.objects.get(user = self.request.user)

        context['profile'] = profile
        return context

    def form_valid(self, form):

        print(form.cleaned_data)

        profile = Profile.objects.get(user = self.request.user)
        form.instance.profile = profile

        user = self.request.user
        form.instance.user = user

        post = super().form_valid(form)

        # image_url = self.request.POST['image_url']
        # if image_url:
        #     Photo.objects.create(post=post, image_url=image_url)

        files = self.request.FILES.getlist('image_uploads')

        for file in files:
            Photo.objects.create(post=post, image_file=file)

        return post

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name ='mini_insta/delete_post_form.html'
    context_object_name = 'post'

    def get_login_url(self):
        return reverse('login')
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        profile= Profile.objects.get(user = self.request.user)
        context['profile']= profile
        return context

    def get_success_url(self):
        return reverse('show_profile') 

class UpdatePostView(LoginRequiredMixin, UpdateView):
    model=Post
    form_class = UpdatePostForm
    template_name='mini_insta/update_post_form.html'

    def get_login_url(self):
        return reverse('login')

class ShowFollowersDetailView(DetailView):
    model=Profile
    template_name= 'mini_insta/show_followers.html'
    context_object_name='followers'


    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user = self.request.user)
        context["follower"] = profile.get_followers()
        return context
    

class ShowFollowingDetailView(DetailView):
    model=Profile
    template_name= 'mini_insta/show_following.html'
    context_object_name='following'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user = self.request.user)

        context["following"] = profile.get_following()
        return context

class ShowFeedView(LoginRequiredMixin, DetailView):
    model=Profile
    template_name='mini_insta/show_feed.html'
    context_object_name='profile'
    def get_login_url(self):
        return reverse('login')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user = self.request.user)
        context["feed"] = profile.get_post_feed()
        return context

    def get_object(self):
        return Profile.objects.get(user = self.request.user)
class SearchView(ListView):
    template_name='mini_insta/search_results.html'

    def dispatch(self, request, *args, **kwargs):
        if 'query' not in self.request.GET:
            profile = Profile.objects.get(user = self.request.user)
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

        context["profile"] = Profile.objects.get(user = self.request.user)
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

class CreateProfileView(CreateView):
    template_name = "mini_insta/create_profile_form.html"
    model = Profile
    form_class = CreateProfileForm
    def get_success_url(self):
            return reverse('show_profile')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["user_form"] = UserCreationForm()#how do i get some form parts 

        return context

    # def get_queryset(self):
            
    #     query = self.request.GET.get('query')
    #     if query:
    #         return Post.objects.filter(caption__icontains=query)
        
    #     return Post.objects.none()

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()

            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

            form.instance.user = user

            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context["user_form"] = user_form
            return self.render_to_response(context)

class FollowProfileView(LoginRequiredMixin, TemplateView):
    template_name = "mini_insta/show_profile.html"
    
    def get_login_url(self):
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reverse('login')
        
        logged_in_profile = Profile.objects.get(user=request.user)
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])

        if logged_in_profile != other_profile:
            Follower.objects.get_or_create(
                profile=other_profile,
                follower_profile=logged_in_profile
            )
        return redirect('show_profile', pk = other_profile.pk)

    
class DeleteFollowProfileView(LoginRequiredMixin, TemplateView):
    def get_login_url(self):
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reverse('login')

        logged_in_profile = Profile.objects.get(user=request.user)
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])

        Follower.objects.filter(
            profile=other_profile,
            follower_profile=logged_in_profile
        ).delete()
        return redirect('show_profile', pk = other_profile.pk)


class LikePostView(LoginRequiredMixin, TemplateView):
    def get_login_url(self):
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reverse('login')

        logged_in_profile = Profile.objects.get(user=request.user)
        post = Post.objects.get(pk=self.kwargs['pk'])

        if logged_in_profile != post.profile:
            Like.objects.get_or_create(
                post=post,
                profile=logged_in_profile
            )
        return redirect('show_post', pk = post.pk)


class DeleteLikePostView(LoginRequiredMixin, TemplateView):

    def get_login_url(self):
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reverse('login')

        logged_in_profile = Profile.objects.get(user=request.user)
        post = Post.objects.get(pk=self.kwargs['pk'])

        Like.objects.filter(
            post=post,
            profile=logged_in_profile
        ).delete()
        return redirect('show_post', pk=post.pk)

    