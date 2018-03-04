from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from mariahealth.models import User
from mariahealth.serializers import UserSerializer


class UserList(APIView):
	"""
	Get users
	"""
	def get(self, request, format=None):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response({'details': 'Get users list', 'data': serializer.data})

class UserDetails(APIView):
	"""
	Get user details
	"""
	def get(self, request, user_id):
		user = UserDetails.get_user_id(user_id)
		serializer = UserSerializer(user, many=False)
		return Response({'details': 'Get user details', 'data': serializer.data})

	def get_user_id(user_id):
		try:
			return User.objects.get(pk=user_id, deleted_at=None)
		except User.DoesNotExist:
			raise NotFound(detail='User not found', code=status.HTTP_404_NOT_FOUND)
