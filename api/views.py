from django.shortcuts import render
from .serializers import (RegisterSerializer, LoginSerializer, UserSerializer, WeatherSerializer)
from rest_framework.generics import GenericAPIView
from .renderers import UserJsonRenderer
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from .models import User, Weather
from .weather import weather
from rest_framework.permissions import AllowAny

# Create your views here.

class SignUpAPIView(GenericAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterSerializer
	permission_classes = [AllowAny,]
	renderer_class = (UserJsonRenderer,)

	def get(self, request):
		serializer = self.serializer_class(self.get_queryset(), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)



class LoginAPIView(GenericAPIView):
	queryset = User.objects.all()
	serializer_class = LoginSerializer
	permission_classes = [AllowAny,]
	renderer_class = (UserJsonRenderer,)

	def get(self, request):
		serializer = self.serializer_class(self.get_queryset(), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)

		return Response(serializer.data, status=status.HTTP_200_OK)



class WeatherAPIView(GenericAPIView):
	serializer_class = WeatherSerializer

	def post(self, request):
		location = request.data['location']
		print(f"location {location}")
		location = location+" weather"
		weath = weather(location)
		print(f"weather => {weath}")
		return Response(weath, status.HTTP_201_CREATED)
