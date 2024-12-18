# auctions/models.py

from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product  # Adjust the import based on your project structure
from django.utils import timezone  # To work with time comparisons
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .utils import schedule_auction_task
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class Auction(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('ended', 'Ended'),
        ('sold', 'Sold'),
        ('locked', 'Locked'),


    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='auctions')
    starting_value = models.DecimalField(max_digits=10, decimal_places=2)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        # Automatically update status based on time
     if self.status not in ['sold', 'locked']:
        if timezone.now() >= self.ending_time:
            self.status = 'ended'
        else:
            self.status = 'active'
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Auction for {self.product.name} by {self.user.name}"

@receiver(post_save, sender=Auction)
def schedule_auction_on_creation(sender, instance, created, **kwargs):
    if created:
        from .utils import schedule_auction_task  # Import dynamically
        if instance.ending_time:
            schedule_auction_task(instance.id, instance.ending_time)