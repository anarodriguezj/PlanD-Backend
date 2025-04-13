from .models import Auction, Category
from .serializers import AuctionListCreateSerializer, AuctionDetailSerializer, CategoryListCreateSerializer, CategoryDetailSerializer
from rest_framework import generics
from django.db.models import Q

class AuctionListCreate(generics.ListCreateAPIView):
    
    '''ListCreateAPIView:
        - Maneja las operaciones de listar (GET) y crear (POST) recursos.
        - Proporciona una lista paginada de recursos y permite la creación de nuevos recursos.
        - Útil para endpoints que necesitan mostrar una lista de recursos y permitir la creación
        de nuevos recursos.'''

    serializer_class = AuctionListCreateSerializer

    def get_queryset(self):

        queryset = Auction.objects.all()
        params = self.request.query_params

        search = params.get('search')
        categoria = params.get('categoria')
        precio_max = params.get('precioMax')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if categoria:
            queryset = queryset.filter(category__name__iexact=categoria)

        if precio_max:
            queryset = queryset.filter(price__lte=precio_max)

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
    
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

class CategoryListCreate(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer