"""Circle views."""

# Django REST Framework
from rest_framework import viewsets, mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.circles import IsCircleAdmin

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle 
from cride.circles.models.membership import MemberShip 


#class CircleViewSet(viewsets.ModelViewSet):
class CircleViewSet(mixins.CreateModelMixin,
					mixins.RetrieveModelMixin,
					mixins.UpdateModelMixin,
					mixins.ListModelMixin,
					viewsets.GenericViewSet
					):
	"""Circle view set.
		


	"""

	#queryset = Circle.objects.all()
	serializer_class  =  CircleModelSerializer
	lookup_field='slug_name'


	# Filters
	filter_backends =(SearchFilter, OrderingFilter, DjangoFilterBackend)
	search_fields =('slug_name', 'name')
	ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'members_limit')
	ordering = ('-members__count', '-rides_offered', '-rides_taken')
	filter_fields = ('verified', 'is_limited')

	def get_queryset(self):
		"""Restrict list to public-only."""
		queryset = Circle.objects.all()
		if self.action =='list':	
			return queryset.filter(is_public=True)
		return queryset

	def get_permissions(self):
		"""Assign permissions based on action."""
		permissions = [IsAuthenticated]
		if self.action in ['update', 'partial_update']:
			permissions.append(IsCircleAdmin)
		return [permission() for permission in permissions]


	def perform_create(self, serializer):
		"""Asign circle admin."""
		circle = serializer.save()
		user = self.request.user
		profile = user.profile 
		MemberShip.objects.create(

			user=user,
			profile = profile,
			circle=circles,
			is_admin=True,
			remaining_invitation=10

		)

                    



"""
Desde nuestra consola, la uthorization realmente solo es un header
http localhost:8000/circles/
http localhost:8000/circles/ "Authorization: Token pastetokenhere" -v

"""

"""
cdrf.co
"""