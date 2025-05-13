from .models import Auction, Category, Bid, Rating, Comment
from .serializers import AuctionListCreateSerializer, AuctionDetailSerializer, CategoryListCreateSerializer, CategoryDetailSerializer, BidListCreateSerializer, BidDetailSerializer, RatingSerializer, CommentSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrAdmin
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone

class AuctionListCreate(generics.ListCreateAPIView):

    serializer_class = AuctionListCreateSerializer

    def get_queryset(self):
        queryset = Auction.objects.all()
        params = self.request.query_params

        search = params.get('search', None)  # Filtro de búsqueda por nombre o descripción
        category = params.get('category', None)  # Usar category 
        max_price = params.get('max_price', None)  # Filtro de precio máximo
        min_price = params.get('min_price', None)  # Filtro de precio mínimo
        is_open = params.get("is_open", None)

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

        # Filtrar por subastas abiertas
        if is_open == "true":
            queryset = queryset.filter(closing_date__gt=timezone.now())
        elif is_open == "false":
            queryset = queryset.filter(closing_date__lte=timezone.now())

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
    
class RatingListCreate(generics.ListCreateAPIView):
    """
    Listar o crear valoraciones para una subasta específica.
    """
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(auction_id=self.kwargs['auction_id'])

    def perform_create(self, serializer):
        auction = Auction.objects.get(id=self.kwargs['auction_id'])
        user = self.request.user
        
        if auction.auctioneer == user:
            raise ValidationError("No puedes valorar tu propia subasta.")

        # Si ya existe una valoración previa, eliminarla antes de guardar la nueva
        previous = Rating.objects.filter(auction=auction, user=user).first()
        if previous:
            previous.delete()

        serializer.save(auction=auction, user=user) # crear nueva valoración

    def post(self, request, auction_id):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar una valoración concreta.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.all()

    def perform_destroy(self, instance):
        instance.delete()


class UserRatingView(APIView):
    """
    Consultar o eliminar la valoración del usuario actual sobre una subasta.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, auction_id):
        auction = get_object_or_404(Auction, id=auction_id)
        rating = Rating.objects.filter(auction=auction, user=request.user).first()
        if rating:
            return Response({"rating": rating.rating}, status=200)
        return Response({"detail": "No has valorado esta subasta"}, status=404)

    def delete(self, request, auction_id):
        auction = get_object_or_404(Auction, id=auction_id)
        rating = Rating.objects.filter(auction=auction, user=request.user).first()
        if rating:
            rating.delete()
            return Response({"detail": "Valoración eliminada correctamente."}, status=204)
        return Response({"detail": "No hay valoración registrada."}, status=404)
    

class CommentListCreate(generics.ListCreateAPIView):
    """
    Listar o añadir comentarios a una subasta.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(auction_id=self.kwargs['auction_id'])

    def perform_create(self, serializer):
        auction = Auction.objects.get(id=self.kwargs['auction_id'])
        user = self.request.user

        # Evitar que el subastador valore su propia subasta
        if auction.auctioneer == user:
            raise ValidationError("No puedes valorar tu propia subasta.")

        # Si ya existe una valoración previa, eliminarla antes de guardar la nueva
        previous = Rating.objects.filter(auction=auction, user=user).first()
        if previous:
            previous.delete()

        serializer.save(auction=auction, user=user)

class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, editar o eliminar un comentario específico.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class UserCommentListView(APIView):
    """
    Obtener todos los comentarios realizados por el usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.filter(user=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)