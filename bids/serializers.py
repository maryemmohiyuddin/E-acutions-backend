# bidding/serializers.py
from rest_framework import serializers
from .models import Bidding
from auctions.models import Auction
from django.utils import timezone
from .models import Transaction

class BiddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bidding
        fields = ['user_id', 'auction_id', 'starting_value', 'bidding_value', 'ending_time']
    
    
    
    def validate_auction(self, auction):
        # Ensure auction exists
        if not Auction.objects.filter(id=auction.id).exists():
            raise serializers.ValidationError("Auction does not exist.")
        return auction
    
    def validate(self, data):
        auction = data.get('auction_id')
        current_time = timezone.now()

        # Ensure the auction's ending time is not in the past
        if auction.ending_time <= current_time:
            raise serializers.ValidationError("The auction has already ended.")
        return data
    
from rest_framework import serializers
from .models import SoldAuction
from auctions.serializers import ProductAuctionSerializer  # Import AuctionSerializer from auctions app
from product.serializers import ProductSerializer  # Import ProductSerializer from product app


class SoldAuctionSerializer(serializers.ModelSerializer):
    auction = ProductAuctionSerializer()  # Use the AuctionSerializer to get auction details, including product info
    auction_status = serializers.CharField(source='auction.status')  # Include auction status
    winning_bid_value = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = SoldAuction
        fields = ['id', 'auction', 'user', 'winning_bid_value', 'auction_status']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'auction', 'amount']

    def validate(self, data):
        # Ensure the auction exists and the auction status is not already "sold"
        auction = data.get('auction')
        if auction.status == 'sold':
            raise serializers.ValidationError("This auction has already been sold.")
        return data