from rest_framework import serializers
from .models import Auction, Category, Bid, Rating, Comment
from django.utils import timezone
from datetime import timedelta
import requests
from django.core.files.base import ContentFile
import os
    
class AuctionListCreateSerializer(serializers.ModelSerializer):

    '''para la lista de subastas (GET /subastas/) y para crear nuevas (POST).'''

    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    def get_average_rating(self, obj):
        return obj.average_rating()
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser un número positivo.")
        return value

    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError("El stock debe ser un número positivo.")
        return value
    
    def validate(self, data):
        creation = data.get('creation_date') or timezone.now()
        closing = data.get('closing_date')

        if closing <= creation:
            raise serializers.ValidationError("La fecha de cierre debe ser posterior a la fecha de creación.")

        if closing < creation + timedelta(days=15):
            raise serializers.ValidationError("La subasta debe durar al menos 15 días.")
        
        return data

class AuctionDetailSerializer(serializers.ModelSerializer):

    ''' para ver detalles (GET /subastas/<id>/), actualizar o eliminar. '''

    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    category = serializers.CharField(source="category.name", read_only=True) 
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = [
            "id", "title", "description", "price", "stock", "brand",
            "thumbnail", "creation_date", "closing_date", "isOpen", "category", "average_rating",
        ]

    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    def get_average_rating(self, obj):
        return obj.average_rating()
    
class CategoryListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name']

class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BidDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = Bid
        fields = ['id', 'auction', 'user', 'amount', 'timestamp']
        read_only_fields = ['id', 'auction', 'user', 'timestamp']

class AuctionSummarySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    isOpen = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ["title", "price", "category", "isOpen"]

    def get_isOpen(self, obj):
        from django.utils import timezone
        return obj.closing_date > timezone.now()


class RatingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    auction = AuctionSummarySerializer(read_only=True)
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user', 'auction']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    auction = AuctionSummarySerializer(read_only=True)
    class Meta:
        model = Comment
        fields ='__all__'
        read_only_fields = ['id', 'creation_date', 'modification_date', 'user', 'auction']  
        

