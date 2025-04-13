from django.db import models
from users.models import CustomUser

class Category(models.Model):

    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        ordering=('id',)

    def __str__(self):
        return self.name


class Auction(models.Model):

    '''Modelo de subasta'''


    title = models.CharField(max_length=150) # Título
    description = models.TextField() # Descripción
    closing_date = models.DateTimeField() # Fecha límie para su cierre
    creation_date = models.DateTimeField() # Fecha de creación
    thumbnail = models.URLField() # Campo de imagen
    price = models.DecimalField(max_digits=10, decimal_places=2) # Precio de salida
    stock = models.IntegerField() # Stock
    rating = models.DecimalField(max_digits=3, decimal_places=2) # Valoración
    category = models.ForeignKey(Category, related_name='subastas', on_delete=models.CASCADE) # Categoría
    brand = models.CharField(max_length=100) # Marca
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE) # Usuario que crea la subasta

    class Meta:
        ordering=('id',) 
    
    def __str__(self):  
        return self.title


class Bid(models.Model):
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Aquí usamos CustomUser
    auction = models.ForeignKey(Auction, related_name='pujas', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.auction.title}"