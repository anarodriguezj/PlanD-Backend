from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer, ChangePasswordSerializer  # Asegúrate de importar el serializer
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class UserRegisterView(generics.CreateAPIView):

    ''' Vista dedicada para el registro de un nuevo usuario.'''

    permission_classes = [AllowAny] # Permiso para cualquier usuario

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):

    ''' Vista para listar todos los usuarios.'''

    permission_classes = [IsAdminUser] # Permiso solo para administradores

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    ''' Vista para ver, actualizar o eliminar un usuario.'''

    permission_classes = [IsAdminUser] # Permiso solo para administradores

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    
class LogoutView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Realiza el logout eliminando el RefreshToken (revocar)"""
        try:
            # Se espera que el refresh token esté en el cuerpo del request
            refresh_token = request.data.get('refresh', None)
            if not refresh_token:
                return Response(
                    {"detail": "No refresh token provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Revocar el RefreshToken
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):

    ''' Vista para ver y editar el perfil del usuario. 
        Implementación personalizada de los métodos GET, PATCH y DELETE.
        El usuario solo tiene acceso a SU PROPIO perfil.'''

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePasswordView(APIView):

    ''' Vista para cambiar la contraseña del usuario (implementación personalizada de POST)
        Se validan los datos (contraseña antigua y nueva) usando el serializer.'''

    permission_classes = [IsAuthenticated]

    def post(self, request):
    
        serializer = ChangePasswordSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():

            if not user.check_password(serializer.validated_data['old_password']):

                return Response(
                    {"old_password": "Incorrect current password."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                validate_password(serializer.validated_data['new_password'], user)

            except ValidationError as e:

                return Response(
                    {"new_password": e.messages},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password updated successfully."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

