# bidding/urls.py
from django.urls import path
from .views import place_bid
from .views import AuctionBidsView
from .views import SoldAndLockedAuctionsView
from .views import create_transaction


urlpatterns = [
    path('place-bid/', place_bid, name='place_bid'),
    path('auction/<int:auction_id>/', AuctionBidsView.as_view(), name='auction-bids-list'),
    path('sold-and-locked-auctions/<int:user_id>/', SoldAndLockedAuctionsView.as_view(), name='sold_and_locked_auctions_by_user'),
    path('createtransaction/', create_transaction, name='create-transaction'),


]
