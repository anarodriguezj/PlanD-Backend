"""
URL configuration for backendSpark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path("admin/", admin.site.urls),
    # redirige todas las URLs que empiecen por /api/subastas/ a otro archivo de rutas dentro de la app subastas
    path("api/subastas/", include("subastas.urls")),
    # redirige todas las URLs que empiecen por /api/users/ a otro archivo de rutas dentro de la app users
    path("api/users/", include("users.urls")),
    # para realizar login (django lo gestiona automáticamente)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
