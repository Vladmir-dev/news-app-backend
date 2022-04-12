from django.urls import path
from .views import (SignUpAPIView, LoginAPIView, WeatherAPIView)


urlpatterns = [
   path('signup/', SignUpAPIView.as_view(), name="signup"),
   path('login/', LoginAPIView.as_view(), name="login"),
   path('weather/', WeatherAPIView.as_view(), name="weather"),
]