"""Rides Urls."""

# Django
from django.urls import include, path


# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views.
#from cride.circles.views import (list_circles, create_circle, create_circle_serializer)
from .views import rides as ride_views



router = DefaultRouter()

router.register(r'circles/(?P<slug_name>[-a-zA-Z0-0_]+)/rides', ride_views.RideViewSet, basename='ride')

urlpatterns = [
	
    path('', include(router.urls))
]


