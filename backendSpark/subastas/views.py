from .models import Auction, Category
from .serializers import AuctionSerializer, AuctionDetailSerializer, CategoryListCreateSerializer, CategoryDetailSerializer
from rest_framework import generics

class AuctionListCreate(generics.ListCreateAPIView):
    
    '''ListCreateAPIView:
        - Maneja las operaciones de listar (GET) y crear (POST) recursos.
        - Proporciona una lista paginada de recursos y permite la creación de nuevos recursos.
        - Útil para endpoints que necesitan mostrar una lista de recursos y permitir la creación
        de nuevos recursos.'''

    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''
    RetrieveUpdateDestroyAPIView:
        - Maneja las operaciones de recuperar (GET), actualizar (PUT) y eliminar (DELETE) un
        recurso individual.
        - Combina las funcionalidades de las vistas RetrieveAPIView, UpdateAPIView y
        DestroyAPIView.
        - Útil para endpoints que necesitan mostrar un recurso específico y permitir su
        actualización y eliminación.'''
    
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

class CategoryListCreate(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer