"""Users View."""

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated
)
from cride.users.permissions import IsAccountOwner 

# Serializers
from cride.circles.models.circles import Circle
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers.users import (

	UserLoginSerializer,
	UserSingupSerializer,
	UserModelSerializer,
	AccountVerificationSerializer

)

from cride.users.serializers.profile import ProfileModelSerializer

# Models
from cride.users.models import User




class UserViewSet(mixins.RetrieveModelMixin,
				mixins.UpdateModelMixin,
				viewsets.GenericViewSet):
	
	"""User view set.
	
	Handle sign up, login and account verification.
	
	"""

	queryset = User.objects.filter(is_active=True, is_client=True)
	serializer_class = UserModelSerializer
	lookup_field = 'username'

	def get_permissions(self):
		"""Assign permissions based on action."""
		if self.action in ['signup', 'login', 'verify']:
			permissions = [AllowAny]
		elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
			permissions = [IsAuthenticated, IsAccountOwner]
		else:
			permissions = [IsAuthenticated]
		return [p() for p in permissions]

	@action(detail=False, methods=['post'])
	def login(self, request):
		"""User sign  in."""
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user, token  = serializer.save()
		data = {
			'user': UserModelSerializer(user).data,
			'access_token':token 
		}
		return Response(data, status=status.HTTP_201_CREATED)

	@action(detail=False, methods=['post'])
	def signup(self, request):
		"""User Sign up."""
		serializer = UserSingupSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = UserModelSerializer(user).data 
		return Response(data, status=status.HTTP_201_CREATED)

	@action(detail=False, methods=['post'])
	def verify(self, request):
		"""Account verification."""
		serializer = AccountVerificationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		data ={'message':'Congratulation, account active'}
		return Response(data, status=status.HTTP_200_OK)

	@action(detail=True, methods=['put', 'patch'])
	def profile(self, request, *args, **kwargs):
		"""Update profile data"""
		user = self.get_object()
		profile = user.profile
		partial = request.method == 'PATCH'
		serializer = ProfileModelSerializer(
			profile,
			data = request.data,
			partial =partial
		)

		serializer.is_valid(raise_exception=True)
		serializer.save()
		data = UserModelSerializer(user).data 
		return Response(data)

		"""
			for loading picture en postman body/form-data in key picture and in value up the file
			cmd = http -f PATCH localhost:8000/users/freddier/profile/ picture@~/pictures/me/fredd.jpg "Authorization : Token " -b
		"""

	def retrieve(self, request, *args, **kwargs):
		"""Add extra data to the response."""
		response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
		circles = Circle.objects.filter(
			members=request.user,
			membership__is_active=True
		)
		data = {
			'user':response.data,
			'circles': CircleModelSerializer(circles, many=True).data
		}

		response.data = data
		return Response(response.data)

class UserLoginApiView(APIView):
	"""User Login API view."""

	def post(self, request, *args, **kwargs):
		"""Handle HTTP POST request."""
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user, token = serializer.save()
		data ={
			'user':UserModelSerializer(user).data,
			'access_token':token
		}

		return Response(data, status=status.HTTP_201_CREATED)

class UserSingupApiView(APIView):
	"""User Login API view."""

	def post(self, request, *args, **kwargs):
		"""Handle HTTP POST request."""
		serializer = UserSingupSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = UserModelSerializer(user).data
		return Response(data, status=status.HTTP_201_CREATED)



class AccountVerificationApiView(APIView):
	"""Account verification API view."""

	def post(self, request, *args, **kwargs):
		"""Handle HTTP POST request."""
		serializer = AccountVerificationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = {'message':'Congratulations, now go share some rides!'}
		return Response(data, status=status.HTTP_200_OK)