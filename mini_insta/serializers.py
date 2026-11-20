from rest_framework import serializers
from .models import Profile, Post, Photo


class PhotoSerializer(serializers.ModelSerializer):
    # Uses your model's helper method if you support both image_url and image_file
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'post', 'image_url', 'timestamp']

    def get_image_url(self, obj):
        return obj.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    # Read-only nested photos; pulls from your existing get_all_photos() method
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'profile', 'caption', 'timestamp', 'photos']
        read_only_fields = ['id', 'profile', 'timestamp']

    def get_photos(self, obj):
        photos = obj.get_all_photos()
        return PhotoSerializer(photos, many=True, context=self.context).data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'display_name',
            'profile_image_url',
            'bio_text',
            'join_date',
        ]
