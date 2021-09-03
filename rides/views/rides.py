"""Rides views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from cride.rides.serializer import CreateRideSerializer

# Models
from cride.circles.models import Circle 


class RideViewSet(mixins.CreateModelMixin,
				  viewsets.GenericViewSet):
	"""Ride view set."""