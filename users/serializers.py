from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    '''Serializer para el modelo CustomUser, para crear y actualizar usuarios.'''

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'birth_date',
            'municipality', 'locality', 'password'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        user = self.instance  # Solo tiene valor cuando se está actualizando
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):

    '''Serializer para cambiar la contraseña del usuario. 
    Se pide al usuario la contraseña antigua y la nueva.'''

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)