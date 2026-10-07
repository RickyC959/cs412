# File: mini_insta/models.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: all the models that are part of this app

from django.db import models
from django.urls import reverse

# Create your models here.


class Profile(models.Model):
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def get_all_posts(self):
        posts = Post.objects.filter(profile=self)
        return posts

    def __str__(self):
        return f'{self.username}, {self.display_name}'


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('post', kwargs={'pk': self.pk})
    
    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos

    def __str__(self):
        return f'{self.profile.username}, {self.caption}, {self.timestamp}'


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.FileField(blank=True)

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url


    def get_url(self):
        return reverse('photo', kwargs={'pk': self.pk})

    def __str__(self):
        if self.image_url: 
            return f'{self.post.caption},URL: {self.image_url}, {self.timestamp}'
        else:
            return f'{self.post.caption},FILE: {self.image_file}, {self.timestamp}'
        
