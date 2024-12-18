# bidding/models.py
from django.db import models
from django.contrib.auth import get_user_model
from auctions.models import Auction  # Import the Auction model from the 'auction' app
import datetime
from django.utils import timezone

User = get_user_model()

class Bidding(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='biddings')  # Foreign key to the User model
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')  # Foreign key to the Auction model
    starting_value = models.DecimalField(max_digits=10, decimal_places=2)  # Decimal field for the starting value
    bidding_value = models.DecimalField(max_digits=10, decimal_places=2)  # Decimal field for the bidding value
    ending_time = models.DateTimeField()

    def __str__(self):
        return f"Bidding {self.id} by {self.user_id}"

    def save(self, *args, **kwargs):
        # Ensure bidding value is greater than starting value before saving
        
        
               
        # Ensure bidding time is before ending time
        if self.ending_time <= timezone.now():
            raise ValueError("The auction is already closed.")


        super().save(*args, **kwargs)  # Call the parent class's save method

class SoldAuction(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='sold_auction')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='won_auctions')  # The winning user
    winning_bid_value = models.DecimalField(max_digits=10, decimal_places=2)  # The winning bid amount

    def __str__(self):
        return f"Auction {self.auction.id} sold to {self.user.username}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')  # Foreign key to the User model
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='transactions')  # Foreign key to the Auction model
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount involved in the transaction
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the transaction was created

    def __str__(self):
        return f"Transaction for Auction {self.auction.id} by {self.user.name}"

    # Optionally, you can add validation to ensure that the transaction amount is positive
    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValueError("Transaction amount must be greater than zero")
        super().save(*args, **kwargs)  # Call the parent class's save method