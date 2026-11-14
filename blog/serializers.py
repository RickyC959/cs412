## file: blog/serializer.py
## converts model data to JSON

from rest_framework import serializers
from .models import *

## a serializer class for the Article object

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'text', 'published', 'image_url']

    ## fixing user foriegn key 

    def create(self, validated_data):

        print(f"ArticleSerializer.create;  validated_data= {validated_data}")

        # create article object
        article = Article(**validated_data)
        article.user = User.objects.first() # admin

        article.save()
        
        return article
