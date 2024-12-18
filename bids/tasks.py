import logging
from celery import shared_task
from datetime import datetime
import pytz
from auctions.models import Auction
from bids.models import Bidding, SoldAuction
from django.utils import timezone
import requests
# Configure logger
logger = logging.getLogger(__name__)

@shared_task
def auction_end_task(auction_id, end_time):
    current_time = timezone.now()
    
    logger.info(f"Starting auction_end_task for auction_id={auction_id}. Current time: {current_time}, End time: {end_time}")
    
    # Check if the auction has ended yet
    if current_time < end_time:
        logger.info(f"Auction {auction_id} has not ended yet. Current time is {current_time}, but end time is {end_time}. Task will not proceed.")
        return  # Do nothing if the auction has not ended yet
    
    if not isinstance(auction_id, int):
        logger.error(f"Invalid auction_id type: {type(auction_id)}. Auction ID must be an integer.")
        return  # If auction_id is not an integer, do nothing
    
    # Get all auctions from the database for debugging purposes
    try:
        all_auctions = Auction.objects.all()
        logger.info(f"Retrieved all auctions. Number of auctions found: {all_auctions.count()} {all_auctions}")

        # Log details for each auction to check what they contain
        for auction in all_auctions:
            logger.info(f"Auction details: id={auction.id}, user={auction.user.name if auction.user else 'N/A'}, "
                        f"product={auction.product.name if auction.product else 'N/A'}, "
                        f"starting_value={auction.starting_value}, starting_time={auction.starting_time}, "
                        f"ending_time={auction.ending_time}, status={auction.status}")
        
        # Now try to find the auction by its ID
        auction = Auction.objects.get(id=auction_id)
        logger.info(f"Auction {auction_id} found: {auction}")
        logger.info(f"Auction details: id={auction.id}, user={auction.user.name if auction.user else 'N/A'}, "
                    f"product={auction.product.name if auction.product else 'N/A'}, "
                    f"starting_value={auction.starting_value}, starting_time={auction.starting_time}, "
                    f"ending_time={auction.ending_time}, status={auction.status}")
    
    except Auction.DoesNotExist:
        logger.warning(f"Auction {auction_id} not found. Task will not proceed.")
        return  # Auction not found, so do nothing
    
    # Check if the auction already has a winner or has been marked as 'locked'
    if auction.status == 'locked':
        logger.info(f"Auction {auction_id} is already marked as 'locked'. Task will not proceed.")
        return  # If the auction is already locked, do nothing

    # Check if there are any bids for the auction
    bids = Bidding.objects.filter(auction_id=auction)
    if not bids.exists():
        logger.info(f"No bids found for auction {auction_id}. Task will not proceed.")
        return  # If no bids exist, do nothing
    
    # Find the highest bid
    highest_bid = bids.order_by('-bidding_value').first()
    logger.info(f"Highest bid found for auction {auction_id}: {highest_bid.bidding_value} by user {highest_bid.user_id.name}")
    logger.info(f"user {auction_id}: {highest_bid.bidding_value} by user {highest_bid.user_id.id}")


    # Create a new record in the lockedAuction table
    SoldAuction.objects.create(
        auction_id=auction_id,
        user_id=highest_bid.user_id.id,  # The winner (highest bidder)
        winning_bid_value=highest_bid.bidding_value,
    )
    logger.info(f"Auction {auction_id} locked to {highest_bid.user_id.name} for {highest_bid.bidding_value}")
    # Update the auction status to 'locked'
    try:
        rows_updated = Auction.objects.filter(id=auction_id).update(status='locked')
        if rows_updated > 0:
            logger.info(f"Auction {auction_id} status successfully updated to 'locked'. Rows affected: {rows_updated}")
            print(f"Auction {auction_id} status successfully updated to 'locked'. Rows affected: {rows_updated}")
        else:
            logger.warning(f"No rows were updated for auction {auction_id}. It might not exist or the status was already 'locked'.")
            print(f"No rows were updated for auction {auction_id}. It might not exist or the status was already 'locked'.")

        notification_data = {
            "flag": "wonByBuyer",
            "user_id": auction.user_id,
            "auction_id": auction.id,
            "price": highest_bid.bidding_value,
            "productname": auction.product.name,  # Now using the fetched product name
            "username": highest_bid.user_id.name
        }

        # Call the notification API (this can be replaced by your internal notification model if desired)
        notification_api_url = "http://127.0.0.1:8000/notifications/create-notification/"  # Update with the correct API URL
        response = requests.post(notification_api_url, data=notification_data)
        print(response)
        # Handle the response if necessary
        if response.status_code == 201:
            print("Notification sent successfully")
        else:
            print(f"Failed to send notification: {response.status_code}")

        notification_data = {
            "flag": "buyerWon",
            "user_id": highest_bid.user_id.id,
            "auction_id": auction.id,
            "price": highest_bid.bidding_value,
            "productname": auction.product.name,  # Now using the fetched product name
            "username": highest_bid.user_id.name

        }

        # Call the notification API (this can be replaced by your internal notification model if desired)
        notification_api_url = "http://127.0.0.1:8000/notifications/create-notification/"  # Update with the correct API URL
        response = requests.post(notification_api_url, data=notification_data)
        print(response)
        # Handle the response if necessary
        if response.status_code == 201:
            print("Notification sent successfully")
        else:
            print(f"Failed to send notification: {response.status_code}")
    except Exception as e:
        logger.error(f"Error updating auction {auction_id} status to 'locked': {e}")
        print(f"Error updating auction {auction_id} status to 'locked': {e}")

