from rest_framework import serializers
from .models import Category, Request


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','description','created_at','updated_at']


class RequestSerializer(serializers.ModelSerializer):

    room_image = serializers.ImageField(use_url=True, required=False, allow_null=True)

    category = CategorySerializer()

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Request
        fields = ['user','title','description','category','room_image','created_at','status']


class RequestPartialUpdateSerializer(serializers.ModelSerializer):
    room_image = serializers.ImageField(use_url=True, required=False, allow_null=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['title', 'description', 'category', 'room_image', 'status']
        partial = True