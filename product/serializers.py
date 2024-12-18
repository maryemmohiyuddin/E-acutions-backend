from rest_framework import serializers
from .models import Product
from categories.models import Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'picture', 'user', 'category', 'width','height','weight','description','subName','yearOfManufacture','Material']
        read_only_fields = ['user']  # User will be set from the request context

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'picture': {'required': False},  # Make the 'picture' field optional
        }
