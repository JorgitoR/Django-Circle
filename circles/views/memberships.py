"""Circle membership views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action # esto es un decorador
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Serializers
from cride.circles.serializers.membership import MembershipModelSerializer, AddMemberSerializer

# Permision
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember, IsSelfMember

# Models
from cride.circles.models import Circle, MemberShip, Invitation

class MembershipViewSet(mixins.ListModelMixin,
						mixins.CreateModelMixin,
						mixins.RetrieveModelMixin,
						mixins.DestroyModelMixin,
						viewsets.GenericViewSet):
	"""Circle membershio view set."""

	serializer_class = MembershipModelSerializer

	def dispatch(self, request, *args, **kwargs):
		"""Verify that the circle exist."""
		slug_name = kwargs['slug_name']
		self.circle = get_object_or_404(Circle, slug_name=slug_name)
		return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

	def get_permissions(self):
		"""Assign permissions based on action."""
		permissions = [IsAuthenticated]
		if self.action != 'create':
			permissions.append(IsActiveCircleMember)
		if self.action == 'invitations':
			permissions.append(IsSelfMember)
		return [p() for p in permissions]

	def get_queryset(self):
		"""Return circle members."""
		return MemberShip.objects.filter(
			circle=self.circle,
			is_active=True
		)

	#{{host}}/circles/slug_name/members/
	def get_object(self):
		"""Return the circle member by using the user's username."""
		#import pdb; pdb.set_trace() #cuando llega al debugger self.args or self.kwargs

		return get_object_or_404(
			MemberShip,
			user__username=self.kwargs['pk'],
			circle = self.circle,
			is_active = True
		)

	#{{host}}/circles/slug_name/members/freddier -- Method Del
	def perform_destroy(self, isntance):
		"""Disable membership."""
		isntance.is_active = False
		isntance.save()


	#{{host}}/circles/slug_name/members/freddier/invitations/
	@action(detail=True, methods=['get'])
	def invitations(self, request, *args, **kwargs):
		"""Retrieve a member's invitations breakdown.

		Will return a list containing all the members that have
		used its invitations and another list containing the 
		invitations that haven't being used yet.

		"""

		member = self.get_object()

		invited_members = MemberShip.objects.filter(
			circle = self.circle,
			invited_by = request.user,
			is_active=True
		)

		unused_invitations = Invitation.objects.filter(
			circle = self.circle,
			issued_by = request.user,
			used=False
		).values_list('code')

		diff = member.remaining_invitation - len(unused_invitations) #diff means diference

		invitations = [x[0] for x in unused_invitations]
		for i in range(0, diff):
			invitations.append(

				Invitation.objects.create(
					issued_by=request.user,
					circle=self.circle
				).code #no queremos agregar una lista de string, solo queremos enviar el code

			)

		data = {
			'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
			'invitations':invitations
		}

		return Response(data)

	"""
		pablo = User.objects.get(username='ptrinidad')
		freddy = User.objects.get(username='freddier')
		fciencias = Circle.objects.get(slug_name='fciencias')

		m= Membership.objects.create(user=pablo, profile=pablo.profile, circle=fciencias, invited_by=freddy)

		len(Invitation.objects.all().values_list('code'))
		2
	"""

	def create(self, request, *args, **kwargs):
		"""Handle member creation from invitation code."""
		print(request)
		serializer = AddMemberSerializer(
        	data=request.data,
        	context={'circle': self.circle, 'request': request}
     	)
		serializer.is_valid(raise_exception=True)
		member = serializer.save()

		data = self.get_serializer(member).data 
		return Response(data, status=status.HTTP_201_CREATED)

		"""
			http localhost:8000/circles/slug_name/members/ invitation_code=HDASBJSKDF "Authorization: Token " -b

			
		"""

