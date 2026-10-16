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

    def get_post_feed(self):

        return Post.objects.filter(profile__in=self.get_following()).order_by('-timestamp')

    def get_followers(self):
            
        follower_records = Follower.objects.filter(profile=self)
        followers_list = [record.follower_profile for record in follower_records]
        
        return followers_list
    
    def get_num_followers(self):
        follower_records = Follower.objects.filter(profile=self)
        return len(follower_records)

    def get_following(self):
        following_records = Follower.objects.filter(follower_profile=self)
        following_list = [record.profile for record in following_records]
        return following_list

    def get_num_following(self):
        following_records = Follower.objects.filter(follower_profile=self)
        return len(following_records)


    def get_absolute_url(self):
            '''Return the URL to display the profile.'''
            return reverse('show_profile', kwargs={'pk': self.pk})

    def get_all_posts(self):
        posts = Post.objects.filter(profile=self)
        return posts

    def get_num_posts(self):
        return len(Post.objects.filter(profile=self))

    def __str__(self):
        return f'{self.username}, {self.display_name}'

class Follower(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="profile")
    follower_profile = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name= "follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f'{self.follower_profile} -> {self.profile}'
   

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)
    def get_profile(self):
        return self.profile
    def get_likes(self):
        return Like.objects.filter(post=self)
    
    def get_num_likes(self):
         return len(Like.objects.filter(post=self))
    
    def get_all_comments(self):
        return Comment.objects.filter(post=self)
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_post', kwargs={'pk': self.pk})
    
    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos

    def __str__(self):
        return f'{self.profile.username}, {self.caption}, {self.timestamp}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return f'From:{self.profile} Comment:{self.text}'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile.username} liked {self.post}'
class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)

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
        
