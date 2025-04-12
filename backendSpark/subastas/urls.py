from django.urls import path
from .views import AuctionListCreate, AuctionRetrieveUpdateDestroy, CategoryListCreate, CategoryRetrieveUpdateDestroy

app_name="subastas"

urlpatterns = [
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),

    # GET /subastas -> Listar subastas (con filtros opcionales)
    # POST /subastas -> Crear nueva subasta
    path('', AuctionListCreate.as_view(), name='auction-list-create'),

    # GET /subastas/<id> -> Obtener una subasta por ID
    # PUT /subastas/<id> -> Actualizar una subasta
    # DELETE /subastas/<id> -> Eliminar una subasta
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail')
]