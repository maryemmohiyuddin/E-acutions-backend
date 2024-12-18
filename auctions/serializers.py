# auctions/serializers.py

from rest_framework import serializers
from .models import Auction
from product.serializers import ProductSerializer

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        productdata = ProductSerializer()  # Include product details

        fields = ['id', 'user', 'product', 'starting_value', 'starting_time', 'ending_time', 'status']

    def validate(self, attrs):
        
        if attrs['starting_time'] >= attrs['ending_time']:
            raise serializers.ValidationError("Ending time must be after starting time.")
        return attrs

class ProductAuctionSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  

    class Meta:
        model = Auction
        fields = ['id', 'user', 'product', 'starting_value', 'starting_time', 'ending_time', 'status']
