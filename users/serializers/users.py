"""Users Serializers."""

#Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token


# Models
from cride.users.models import User
from cride.users.models import Profile

# Utilities
from datetime import timedelta

# Serializers
from cride.users.serializers.profile import ProfileModelSerializer

from cride.mail.email import send_mail_async as send_mail
from cride.mail.settings_email import MTASKS_EMAIL_WITH_URL

import jwt


class UserModelSerializer(serializers.ModelSerializer):
	"""User model Serializer."""

	profile = ProfileModelSerializer(read_only=True)

	class Meta:
		"""Meta class."""

		model = User 
		fields = (

			'username',
			'first_name',
			'last_name',
			'email',
			'phone_number',
			'profile'

		)

class UserSingupSerializer(serializers.Serializer):
	"""User sign up serializer.

	Handle sign up data validation and user/profile creation
	"""
	email = serializers.EmailField(
		validators=[UniqueValidator(queryset=User.objects.all())]
	)

	username =serializers.CharField(
		min_length=4,
		max_length=20,           
		validators=[UniqueValidator(queryset=User.objects.all())]
	)

	# Phone number
	phone_regex= RegexValidator(
		regex=r'\+?1?\d{9,15}$',
		message="Phone number must be entered in the format: +9999999999. Up to 15 digits allowed"
	)
	phone_number = serializers.CharField(validators=[phone_regex])

	# password
	password = serializers.CharField(min_length=8, max_length=64)
	password_confirmation = serializers.CharField(min_length=8, max_length=64)

	# Name
	first_name = serializers.CharField(min_length=2, max_length=30)
	last_name = serializers.CharField(min_length=2, max_length=30)

	#http localhost:8000/users/singup/ email=jorgitouribe133@gmail.com username=mark phone_number=+523157046849 password=jorgeluiz password_confirmation=jorgeluiz first_name=markk last_name=sfd
	#http localhost:8000/users/login/ email= password
	#http localhost:8000/users/verify/ token=

	def validate(self, data):
		"""Verify passwords match."""
		passw = data['password']
		passw_conf = data['password_confirmation']
		if passw != passw_conf:
			raise serializers.ValidationError("Passwords don't match.")
		password_validation.validate_password(passw)
		return data
		

	def create(self, data):
		"""Handle user and profile creation."""
		data.pop('password_confirmation') #sacamos password confirmation
		user = User.objects.create_user(**data, is_verified=False)
		Profile.objects.create(user=user)
		self.send_confirmation_email(user)
		return user

	def send_confirmation_email(self, user):
		"""Send account verification link to given user."""
		verification_token = self.get_verification_token(user)
		subject = 'Welcom @{} Verify your account to start using Comparte Ride'.format(user.username)
		from_email = 'Comparte Ride <communitytask485@gmail.com>'
		content = render_to_string(
			'email/users/account_verification.html',
			{'token':verification_token, 'user':user}
		)

		values = {

				"id": verification_token,
				"usuario": user,
				"titulo": verification_token,
				"descripcion": 'token',
				"sign": 'Token',

		}

		send_mail(

				'Dev Django Nueva Tarea Creada',
				MTASKS_EMAIL_WITH_URL.format(**values),
				from_email,
				[user.email],

		)

	def get_verification_token(self, user):
		"""Create JWT token that the user can use to verify its account."""
		
		exp_date = timezone.now() + timedelta(days=3)
		payload = {

			'user':user.username,
			'exp': int(exp_date.timestamp()),
			'type': 'email_confirmation'

		}

		token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
		return token

	# Token =
	# jwt.decode(Token, settings.SECRET_KEY, algorithms=['HS256']) 


class UserLoginSerializer(serializers.Serializer):
	"""User Login serializer.

	Handle the login request data.
	"""

	email = serializers.EmailField()
	password = serializers.CharField(min_length=9, max_length=64)

	def validate(self, data):
		"""Check credentials."""
		user = authenticate(username=data['email'], password=data['password'])
		if not user:
			raise serializers.ValidationError('Invalid credentials')
		if not user.is_verified:
			raise serializers.ValidationError('Account is not active yet :(')
		self.context['user']=user
		return data

	def create(self, data):
		"""Generate or retrieve new token"""
		token, created = Token.objects.get_or_create(user=self.context['user'])

		#Token.objects.get(user__username='devvv')

		return self.context['user'], token.key

		
class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
