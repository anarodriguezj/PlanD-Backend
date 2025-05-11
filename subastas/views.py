from .models import Auction, Category, Bid
from .serializers import AuctionListCreateSerializer, AuctionDetailSerializer, CategoryListCreateSerializer, CategoryDetailSerializer, BidListCreateSerializer, BidDetailSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrAdmin
from rest_framework.exceptions import ValidationError

class AuctionListCreate(generics.ListCreateAPIView):
    serializer_class = AuctionListCreateSerializer

    def get_queryset(self):
        queryset = Auction.objects.all()
        params = self.request.query_params

        search = params.get('search', None)  # Filtro de búsqueda por nombre o descripción
        category = params.get('category', None)  # Usar category 
        max_price = params.get('max_price', None)  # Filtro de precio máximo
        min_price = params.get('min_price', None)  # Filtro de precio mínimo
        
        print(f"Search: {search}, Category: {category}, Max Price: {max_price}, Min Price: {min_price}")

        # Filtrar por término de búsqueda
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        # Filtrar por categoría (ahora usamos category.id)
        if category:
            queryset = queryset.filter(category__id=category)

        # Filtrar por precio mínimo
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                pass  # Si no es un valor numérico válido, ignoramos el filtro

        # Filtrar por precio máximo
        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                pass  # Si no es un valor numérico válido, ignoramos el filtro

        return queryset


class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''
    RetrieveUpdateDestroyAPIView:
        - Maneja las operaciones de recuperar (GET), actualizar (PUT) y eliminar (DELETE) un
        recurso individual.
        - Combina las funcionalidades de las vistas RetrieveAPIView, UpdateAPIView y
        DestroyAPIView.
        - Útil para endpoints que necesitan mostrar un recurso específico y permitir su
        actualización y eliminación.'''
    
    permission_classes = [IsOwnerOrAdmin]
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

class CategoryListCreate(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class BidListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        return Bid.objects.filter(auction_id=self.kwargs['auction_id']).order_by('-amount')

    def perform_create(self, serializer):
        auction = Auction.objects.get(pk=self.kwargs['auction_id']) 
        
        if auction.auctioneer.id == self.request.user.id:
            print("Error: El usuario está intentando pujar en su propia subasta.")  # Agregar log aquí
            raise ValidationError("No puedes pujar en tu propia subasta.")
        
        serializer.save(auction=auction, user=self.request.user)


class UserBidListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

class BidDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BidDetailSerializer

    def get_queryset(self):
        return Bid.objects.filter(auction_id=self.kwargs['auction_id']) 
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class UserAuctionListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Obtener las subastas del usuario autenticado
        user_auctions = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(user_auctions, many=True)
        return Response(serializer.data)