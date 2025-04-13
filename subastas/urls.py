from django.urls import path
from .views import (
    AuctionListCreate,
    AuctionRetrieveUpdateDestroy, 
    CategoryListCreate, 
    CategoryRetrieveUpdateDestroy, 
    UserAuctionListView, 
    UserBidListView, 
    BidListCreateView, 
    BidDetailView,
    )


app_name="subastas"

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),

    # Auctions
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),

    # Bids
    path('<int:auction_id>/bid', BidListCreateView.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bid/<int:pk>', BidDetailView.as_view(), name='bid-detail'),

    # Users
    path('users/', UserAuctionListView.as_view(), name='action-from-users'),
    path("users/bids/", UserBidListView.as_view(), name="user-bid-list"),
]