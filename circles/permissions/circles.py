"""Circles permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import MemberShip

class IsCircleAdmin(BasePermission):
	"""Allow acces. Only to circle admins."""

	def has_object_permission(self, request, view, obj):
		"""Verify user have a membership in the obj."""
		try:
			MemberShip.objects.get(
				user=request.user,
				circle=obj,
				is_admin=True,
				is_active=True

			)

		except MemberShip.DoesNotExist:
			return False
		return True
		