"""Rides models."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel

class Ride(CRideModel):
	"""Ride Model."""

	offered_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
	offered_in = models.ForeignKey('circles.Circle', on_delete=models.SET_NULL, null=True)

	passangers = models.ManyToManyField('user.User', related_name='passangers')

	available_seats = models.PositiveSmallIntegerField(default=1)
	comments = models.TextField(blank=True)

	departure_locaion = models.CharField(max_length=255)
	departure_date = models.DateTimeField()
	arrival_location = models.CharField(max_length=255)
	arrival_date = models.DateTimeField()

	rating = models.FloatField(null=True)

	is_active = models.BooleanField(
		'active status',
		default=True,
		help_text='Used for disabling the ride or marking it as finished'
	)