# auctions/urls.py

from django.urls import path
from .views import AuctionCreateView, AuctionListView, AuctionDetailView
from .views import AuctionListWithProductsView

urlpatterns = [
    path('create/', AuctionCreateView.as_view(), name='auction-create'),
    path('list/', AuctionListView.as_view(), name='auction-list'),  # URL for listing all auctions
    path('<int:id>/', AuctionDetailView.as_view(), name='auction-detail'),  # URL for viewing a single auction by ID
    path('auctions-with-products/', AuctionListWithProductsView.as_view(), name='auction-list-with-products'),

]
