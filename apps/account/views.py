from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, mixins, status, viewsets
from djoser.conf import settings
from http import HTTPStatus

from .models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import  UserSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.request import Request
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.utils import OpenApiParameter, extend_schema

from djoser.views import UserViewSet as UVS




# Create your views here.
"""USER VIEW"""
@extend_schema(summary="Users", tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    #authentication_classes = [] #disables authentication
    #permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    print("chamou user viewset")
    #http_method_names = ['get', 'post',]


"""LOGIN VIEW"""
@extend_schema(summary="Get the token", tags=['Login'])
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        serializer.validated_data['status'] = "sucess"
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


"""CHANGE PASSWORD VIEW"""
@extend_schema(summary="Users", tags=['Users'])
class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = CustomTokenObtainPairSerializer.get_token(user)

        return Response({'refresh': str(refresh),
            'access': str(refresh.access_token),'status':'sucess',
            "id_usuario":str(user.id_usuario) }, status=status.HTTP_200_OK)

@extend_schema(summary="DJOSER", tags=['DJOSER'])
class CustomSignupView(UVS):
    http_method_names = ['get', 'post', 'head']
    @action([""], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = {'message': 'List function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)