from rest_framework import serializers
from .models import Auction, Category, Bid
from django.utils import timezone
from datetime import timedelta
    
class AuctionListCreateSerializer(serializers.ModelSerializer):

    '''para la lista de subastas (GET /subastas/) y para crear nuevas (POST).'''

    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser un número positivo.")
        return value

    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError("El stock debe ser un número positivo.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La valoración debe estar entre 1 y 5.")
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

    class Meta:
        model = Auction
        fields = [
            "id", "title", "description", "price", "rating", "stock", "brand",
            "thumbnail", "creation_date", "closing_date", "isOpen", "category"
        ]

    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
class CategoryListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name']

class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class BidListCreateSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'user', 'amount', 'timestamp']
        read_only_fields = ['id', 'auction', 'user', 'timestamp']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class BidDetailSerializer(serializers.ModelSerializer):
    
    user = serializers.CharField(source="user.username", read_only=True)


    class Meta:
        model = Bid
        fields = ['id', 'auction', 'user', 'amount', 'timestamp']
        read_only_fields = ['id', 'auction', 'user', 'timestamp']
