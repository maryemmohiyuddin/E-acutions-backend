# bidding/views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Bidding
from .serializers import BiddingSerializer
from auctions.models import Auction
from django.utils import timezone
from rest_framework import generics
from .serializers import TransactionSerializer
import requests  # Import the requests library to call the external API
from django.contrib.auth import get_user_model

from product.models import Product
User = get_user_model()

@api_view(['POST'])
def create_transaction(request):
    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        print("requst.data", request.data)

        if serializer.is_valid():
            # Create the transaction
            transaction = serializer.save()

            # Get the associated auction and update its status to 'sold'
            auction = Auction.objects.get(id=transaction.auction.id)
            try:
                rows_updated = Auction.objects.filter(id=transaction.auction.id).update(status='sold')
                if rows_updated > 0:
                    print(f"Auction {transaction.auction.id} status successfully updated to 'sold'. Rows affected: {rows_updated}")
                    user = User.objects.get(id=request.data.get('user'))

                    notification_data = {
                        "flag": "soldToBuyer",
                        "user_id": auction.user_id,
                        "auction_id": auction.id,
                        "price": request.data.get('amount'),  # Assuming amount comes from the request body
                        "productname": auction.product.name,  # Now using the fetched product name
                        "username": user.name
                    }

        # # Call the notification API (this can be replaced by your internal notification model if desired)
                    notification_api_url = "http://127.0.0.1:8000/notifications/create-notification/"  # Update with the correct API URL
                    response = requests.post(notification_api_url, data=notification_data)
                    print(response)
                    # Handle the response if necessary
                    if response.status_code == 201:
                        print("Notification sent successfully")
                    else:
                        print(f"Failed to send notification: {response.status_code}")

                    notification_data = {
                        "flag": "buyerPurchased",
                        "user_id": user.id,
                        "auction_id": auction.id,
                        "price": request.data.get('amount'),  # Assuming amount comes from the request body
                        "productname": auction.product.name,  # Now using the fetched product name
                        "username": user.name
                    }

                    # # Call the notification API (this can be replaced by your internal notification model if desired)
                    notification_api_url = "http://127.0.0.1:8000/notifications/create-notification/"  # Update with the correct API URL
                    response = requests.post(notification_api_url, data=notification_data)
                    print(response)
                    # Handle the response if necessary
                    if response.status_code == 201:
                        print("Notification sent successfully")
                    else:
                        print(f"Failed to send notification: {response.status_code}")

                        
                else:
                    print(f"No rows were updated for auction {transaction.auction.id}. It might not exist or the status was already 'sold'.")
            except Exception as e:
                print(f"Error updating auction {transaction.auction.id} status to 'sold': {e}")

            # Return a successful response
            return Response({"message": "Transaction created successfully and auction marked as sold."}, status=status.HTTP_201_CREATED)

        # If the serializer is not valid, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def place_bid(request):
    """
    API view for placing a bid on an auction.
    Validates the bid and auction details before creating the bid.
    """
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Get data from request
    user = request.user
    auction_id = request.data.get('auction_id')
    bidding_value = request.data.get('bidding_value')

    try:
        auction = Auction.objects.get(id=auction_id)
    except Auction.DoesNotExist:
        return Response({"detail": "Auction does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # Check if auction has ended
    if timezone.now() > auction.ending_time:
        return Response({"detail": "Auction has already ended."}, status=status.HTTP_400_BAD_REQUEST)

    # Check the highest bid for this auction
    highest_bid = Bidding.objects.filter(auction_id=auction_id).order_by('-bidding_value').first()
    
    if highest_bid and int(bidding_value) <= int(highest_bid.bidding_value):
        return Response({
            "detail": f"Your bid must be higher than the current highest bid of {int(highest_bid.bidding_value)}."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the bid is at least higher than the starting value of the auction
    if int(float(auction.starting_value)) > int(bidding_value):
        return Response({
            "detail": f"Your bid must be equal to or higher than the starting value of {int(float(auction.starting_value))}."
        }, status=status.HTTP_400_BAD_REQUEST)

    
    # Create the Bidding instance
    bidding_data = {
        'user_id': user.id,
        'auction_id': auction_id,
        'starting_value': auction.starting_value,
        'bidding_value': bidding_value,
        'ending_time': auction.ending_time,
    }

    serializer = BiddingSerializer(data=bidding_data)

    if serializer.is_valid():
        # Save the bid if all validations pass
        bid = serializer.save()
        try:
            product = Product.objects.get(id=auction.product_id)  # Fetch product using the auction's product_id
            product_name = product.name  # Assuming the Product model has a 'name' field
        except Product.DoesNotExist:
            return Response({"detail": "Product for this auction does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        notification_data = {
            "flag": "gotBid",
            "user_id": auction.user_id,
            "auction_id": auction.id,
            "price": bidding_value,
            "productname": product_name,  # Now using the fetched product name
            "username": user.name
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
        
        return Response({"detail": "Bid placed successfully!"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuctionBidsView(generics.ListAPIView):
    serializer_class = BiddingSerializer

    def get_queryset(self):
        # Get the auction id from the URL parameters
        auction_id = self.kwargs['auction_id']
        # Order by the amount in descending order (highest bid first)
        return Bidding.objects.filter(auction_id=auction_id).order_by('-bidding_value')
from rest_framework.views import APIView
from .models import SoldAuction
from .serializers import SoldAuctionSerializer

class SoldAndLockedAuctionsView(APIView):
    def get(self, request, user_id):
        # Filter SoldAuction by user and auction status (locked or sold)
        sold_auctions = SoldAuction.objects.filter(
            user_id=user_id,
            auction__status__in=['locked', 'sold']  # Filter by auction status
        )
        
        # Serialize the data using the SoldAuctionSerializer
        serializer = SoldAuctionSerializer(sold_auctions, many=True)
        
        # Return the serialized data in the response
        return Response(serializer.data, status=status.HTTP_200_OK)
    

