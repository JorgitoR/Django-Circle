"""Users Urls."""

# Django
from django.urls import path, include

# Views.
from cride.users.views.users import UserLoginApiView, UserSingupApiView, AccountVerificationApiView
from cride.users.views.users import UserViewSet

# Django REST Framework
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
	
	path('users/login/', UserLoginApiView.as_view(), name='login'),
	path('users/singup/', UserSingupApiView.as_view(), name='singup'),
	path('users/verify/', AccountVerificationApiView.as_view(), name='verify'),

	path('', include(router.urls))
]