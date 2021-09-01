"""User models admin."""

#Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from cride.users.models import User, Profile

class CustomUserAdmin(UserAdmin):
	"""User Model Admin."""

	list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client', 'is_verified')
	list_filter = ('is_client', 'is_staff', 'created', 'modified')


class ProfileAdmin(admin.ModelAdmin):
	"""Profile model Admin"""

	list_display = ('users', 'reputation', 'rides_taken', 'rides_offered')
	search_fields = ('users__username', 'users__email')
	list_filter =('reputation',)


admin.site.register(User, UserAdmin)