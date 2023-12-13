
from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


### USERS
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs= {
            'email' : {'write_only': False},
        }
        fields = '__all__'
        

### GET TOKEN
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token['name'] = user.username
        token['email'] = user.email
        #token['user_id'] = user.id_usuario
        return token
    
    def validate(self, attrs):
        # # The default result (access/refresh tokens)
        """ Outra forma de fazer o mesmo retorno:
        data = super().validate(attrs)
        # Add custom data from your user model here
        user = self.user
        data['user_id'] = user.id
        data['user_username'] = user.username
        # Add more custom data fields as needed
        """
        
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        print(self.user)
        dir(attrs)
        data.update({'id_usuario': self.user.id_usuario})
        # and everything else you want to send in the response
        return data
   
### CHANGE PASSWORD    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Senha anterior incorreta, tente novamente')
            )
        return value
    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'senhas_diferentes':("As senhas não correspondem")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data
    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

