"""Circle Urls."""

# Django
from django.urls import include, path


# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views.
#from cride.circles.views import (list_circles, create_circle, create_circle_serializer)
from .views import circles as circle_views
from .views import memberships as membership_views


router = DefaultRouter()
router.register(r'circles', circle_views.CircleViewSet, basename='circle')
router.register(r'circles/(?P<slug_name>[-a-zA-Z0-0_]+)/members', membership_views.MembershipViewSet, basename='membership')

urlpatterns = [
	
	#path('lis_circles/', list_circles),
	#path('lis_circles/create/', create_circle),
	#path('list/create/', create_circle_serializer),

	
    path('', include(router.urls))
]


