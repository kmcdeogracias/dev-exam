from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response


class SystemHealthChecker(APIView):
	"""
	Checks system health
	"""
	def get(self, format=None):
		return Response({'message': 'OK'})