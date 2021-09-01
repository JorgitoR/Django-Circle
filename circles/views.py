#httpie para utilizar el curl en la consola

"""Circles View."""

# Django
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Models
from cride.circles.models.circles import Circle

# Serializers
from cride.circles.serializers import (CircleSerializer, CreateCircleSerializer)

@api_view(['GET'])
def list_circles(request):
	"""List Circles."""


	circles = Circle.objects.filter(is_public=True)
	data = []
	for circle in circles:
		serializer = CircleSerializer(circle)
		data.append(serializer.data)
	#return Response(data)
	return Response(data, safe=False)


@api_view(['GET'])
def list_circles(request):
	"""List Circles."""
	circles = Circle.objects.filter(is_public=True)
	serializer = CircleSerializer(circles, many=True)
	return Response(serializer.data)



@api_view(['POST'])
def create_circle_serializer(request):
	"""Create Circle."""
	serializer = CreateCircleSerializer(data=request.data)
	serializer.is_valid(raise_exception=True) #si no es valido nos envia una excepcion
	#data = serializer.data
	circle = serializer.save()
	#circle = Circle.objects.create(**data) #usamos el desenpaquetado de python
	#return Response(data)
	return Response(CircleSerializer(circle).data)

@api_view(['POST'])
def create_circle(request):
	"""Create Circle."""
	name = request.data['name']
	slug_name=request.data['slug_name']
	about = request.data('about', '')
	circle = Circle.objects.create(name=name, slug_name=slug_name, about=about)
	data={

			'name':circle.name,
			'slug_name':circle.slug_name,
			'rides_taken':circle.rides_taken,
			'rides_offered':circle.rides_offered,
			'members_limit':circle.members_limit,

	}

	return Response(data)