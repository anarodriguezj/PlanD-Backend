from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):

    '''Modelo de categoría'''

    name = models.CharField(max_length=50, blank=False, unique=True) # Nombre de la categoría

    class Meta:
        ordering=('id',)

    def __str__(self):
        return self.name


class Auction(models.Model):

    '''Modelo de subasta'''

    title = models.CharField(max_length=150) # Título
    description = models.TextField() # Descripción
    closing_date = models.DateTimeField() # Fecha límie para su cierre
    creation_date = models.DateTimeField(auto_now_add=True) # Fecha de creación
    thumbnail = models.URLField() # Campo de imagen
    price = models.DecimalField(max_digits=10, decimal_places=2) # Precio de salida
    stock = models.IntegerField() # Stock
    category = models.ForeignKey(Category, related_name='subastas', on_delete=models.CASCADE) # Categoría
    brand = models.CharField(max_length=100) # Marca
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE) # Usuario que crea la subasta

    class Meta:
        ordering=('id',) 

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 2)
        return 1

    
    def __str__(self):  
        return self.title


class Bid(models.Model):

    '''Modelo de puja'''
    
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Cantidad que se puja
    timestamp = models.DateTimeField(auto_now_add=True) # Fecha en la que se hace la puja
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # Usuario que puja
    auction = models.ForeignKey(Auction, related_name='pujas', on_delete=models.CASCADE) # Subasta a la que se puja

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.auction.title}"
    
class Rating(models.Model):

    '''Modelo de valoración'''

    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # Valoración
    auction = models.ForeignKey(Auction, related_name="ratings", on_delete= models.CASCADE) # Subasta que se valora
    user = models.ForeignKey(CustomUser, related_name="ratings", on_delete=models.CASCADE) # Usuario que valora
    
    class Meta:
        ordering=('id',)

    def __str__(self):
        return f"{self.user.username} rated {self.rating} for {self.auction.title}" 

class Comment(models.Model):

    '''Modelo de comentario'''

    title = models.CharField(max_length=200) # Título
    text = models.TextField() # Texto
    auction = models.ForeignKey(Auction, related_name="comments", on_delete=models.CASCADE,) # Subasta sobre la que se comenta
    user = models.ForeignKey(CustomUser, related_name="comments", on_delete=models.CASCADE) # Usuario que comenta
    creation_date = models.DateTimeField(auto_now_add=True) # Fecha de creación
    modification_date = models.DateTimeField(auto_now=True) # Fecha de modificación
    
    def __str__(self):
        return f"{self.user.username} commented {self.title} for {self.auction.title}" 