# notifications/utils.py
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

def create_notification(flag, productname, username, price, user_id):
    try:
        # Get the user object by user_id
        user = User.objects.get(id=user_id)

        # Determine the message based on the flag
        if flag == 'wonByBuyer':
            message = f"Your product {productname} is won by {username} at price of Rs.{price}"
        elif flag == 'soldToBuyer':
            message = f"Your product {productname} is sold to {username} at a price of Rs.{price}"
        elif flag == 'auctionEnded':
            message = f"Your auction for product {productname} has been ended without any winning user."
        elif flag == 'gotBid':
            message = f"You have got a bid of Rs.{price} on product {productname} by {username}."
        elif flag == 'buyerWon':
            message = f"You won the product {productname} in auction with highest bid of Rs.{price}. Pay the price to buy it."
        elif flag == 'buyerPurchased':
            message = f"You have successfully purchased product {productname} at a price of Rs.{price}."
        else:
            raise ValueError("Unknown flag")

        # Create the notification object and save it
        notification = Notification(
            user=user,
            notification=message,
        )
        notification.save()

    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")
    except ValueError as e:
        print(f"Error: {e}")
