"""Circle models admin."""

#Django
from django.contrib import admin

# Models
from cride.circles.models.circles import Circle
from cride.circles.models.membership import MemberShip

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
	"""Circle admin."""

	list_display = [

		"name",
		"verified",
		"is_public",
		"is_limited",
		"members_limit"
	]

	search_fields = ('slug_name', 'name')
	list_filter=(
		'is_public',
		'verified',
		'is_limited'
	)

@admin.register(MemberShip)
class MemberAdmin(admin.ModelAdmin):
	"""MemberShip Admin."""

	list_display = [
		'user',
		'circle'
	]

	search_fields = ('user', 'profile')