from django.db import models

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
    
    class Meta:
        ordering=('id',) 
    
    def __str__(self):  
        return self.title

class Bid(models.Model):

    '''Modelo de puja'''
    
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Precio de la puja
    timestamp = models.DateTimeField(auto_now_add=True) # Fecha de creación la puja
    user = models.CharField(max_length=100) # Pujador 
    auction = models.ForeignKey(Auction, related_name='pujas', on_delete=models.CASCADE) # Identificador de la subasta a la que pertenece la puja

    class Meta:
        ordering=('id',)

    def __str__(self):
        return f"{self.user} bid {self.amount} on {self.auction.title}"
    