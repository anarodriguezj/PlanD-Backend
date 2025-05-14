from django.urls import path
from .views import (
    AuctionListCreate,
    AuctionRetrieveUpdateDestroy, 
    CategoryListCreate, 
    CategoryRetrieveUpdateDestroy, 
    UserAuctionListView, 
    UserBidListView, 
    BidListCreate,
    BidRetrieveUpdateDestroy,
    RatingListCreate,
    RatingRetrieveUpdateDestroy,
    UserRatingView,
    UserRatingListView,
    CommentListCreate,
    CommentRetrieveUpdateDestroy,
    UserCommentListView,
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
    path('<int:auction_id>/bid', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bid/<int:pk>', BidRetrieveUpdateDestroy.as_view(), name='bid-detail'),

    # Users
    path('users/', UserAuctionListView.as_view(), name='action-from-users'),
    path("users/bids/", UserBidListView.as_view(), name="user-bid-list"),
    path('users/comments/', UserCommentListView.as_view(), name='user-comment-list'),
    path('users/ratings/', UserRatingListView.as_view(), name='user-rating-list'),
    
    # Ratings
    path('<int:auction_id>/ratings/', RatingListCreate.as_view(), name='rating-list-create'),
    path('<int:auction_id>/ratings/<int:pk>/', RatingRetrieveUpdateDestroy.as_view(), name='rating-detail'),
    path('<int:auction_id>/ratings/user/', UserRatingView.as_view(), name='user-rating'),
    
    # Comments
    path('<int:auction_id>/comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('<int:auction_id>/comments/<int:pk>/', CommentRetrieveUpdateDestroy.as_view(), name='comment-detail'),  
    # path('<int:auction_id>/comments/user/', UserCommentListView.as_view(), name='user-comments'),
]