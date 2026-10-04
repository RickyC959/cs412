# blog/models.oy
from django.db import models
from django.urls import reverse


class Article(models.Model):
    ''''''
    # define the data attributes of the Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('article', kwargs={'pk': self.pk})

    def get_all_comments(self):
        comments = Comment.objects.filter(article=self)
        return comments


class Comment(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text}'
