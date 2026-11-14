from rest_framework import serializers
from .models import Joke, Picture


class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'timestamp']
        read_only_fields = ['id', 'timestamp']
