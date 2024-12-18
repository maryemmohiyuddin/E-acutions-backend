from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .utils import schedule_auction_task
import requests
from .models import Auction
from .serializers import AuctionSerializer, ProductAuctionSerializer


class AuctionCreateView(generics.CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create auctions

    def perform_create(self, serializer):
        # Set the user from the request and save the auction
        auction = serializer.save(user=self.request.user)
        
        # Call the schedule_auction_task function
        # Assuming `end_time` is part of the auction object
        # You might want to change this to the correct field from your serializer
        # schedule_auction_task(auction.id, auction.ending_time)
        
        # if self.ending_time:
        #     schedule_auction_task(self.id, self.ending_time)


class AuctionListView(generics.ListAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Authenticated or read-only for public

    def get_queryset(self):
        # Dynamically update auction status
        auctions = Auction.objects.all()
        for auction in auctions:
            if auction.status not in ['sold', 'locked']:

                if timezone.now() >= auction.ending_time:
                    if auction.status != 'ended':
                        auction.status = 'ended'
                        auction.save()
                        notification_data = {
                                "flag": "auctionEnded",
                                "user_id": auction.user_id,
                                "auction_id": auction.id,
                                "productname": auction.product.name,  
                            }

                        notification_api_url = "http://127.0.0.1:8000/notifications/create-notification/"  # Update with the correct API URL
                        response = requests.post(notification_api_url, data=notification_data)
                        print(response)
                        # Handle the response if necessary
                        if response.status_code == 201:
                            print("Notification sent successfully")
                        else:
                            print(f"Failed to send notification: {response.status_code}")
                else:
                    if auction.status != 'active':
                        auction.status = 'active'
                        auction.save()
        return auctions


class AuctionDetailView(generics.RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    lookup_field = 'id'  # Retrieves auction based on the ID field
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        auction = super().get_object()
        # Dynamically update status when the detail view is accessed
        if auction.status not in ['sold', 'locked']:

            if timezone.now() >= auction.ending_time:
                if auction.status != 'ended':
                    auction.status = 'ended'
                    auction.save()
                    notification_data = {
                                "flag": "auctionEnded",
                                "user_id": auction.user_id,
                                "auction_id": auction.id,
                                "productname": auction.product.name,  
                            }

                    notification_api_url = "http://127.0.0.1:8000/notifications/create-notification/"  # Update with the correct API URL
                    response = requests.post(notification_api_url, data=notification_data)
                    print(response)
                        # Handle the response if necessary
                    if response.status_code == 201:
                            print("Notification sent successfully")
                    else:
                            print(f"Failed to send notification: {response.status_code}")
            else:
                if auction.status != 'active':
                    auction.status = 'active'
                    auction.save()
        return auction


class AuctionListWithProductsView(generics.ListAPIView):
    serializer_class = ProductAuctionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Authenticated or read-only for public

    def get_queryset(self):
        # Dynamically update auction status
        auctions = Auction.objects.all()
        for auction in auctions:
            if auction.status not in ['sold', 'locked']:

                if timezone.now() >= auction.ending_time:
                    if auction.status != 'ended':
                        auction.status = 'ended'
                        auction.save()
                        notification_data = {
                                "flag": "auctionEnded",
                                "user_id": auction.user_id,
                                "auction_id": auction.id,
                                "productname": auction.product.name,  
                            }

                        notification_api_url = "http://127.0.0.1:8000/notifications/create-notification/"  # Update with the correct API URL
                        response = requests.post(notification_api_url, data=notification_data)
                        print(response)
                        # Handle the response if necessary
                        if response.status_code == 201:
                            print("Notification sent successfully")
                        else:
                            print(f"Failed to send notification: {response.status_code}")
                else:
                    if auction.status != 'active':
                        auction.status = 'active'
                        auction.save()
        return auctions
