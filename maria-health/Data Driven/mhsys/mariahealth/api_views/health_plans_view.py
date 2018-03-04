from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from mariahealth.models import HealthPlan
from mariahealth.serializers import HealthPlanSerializer

class HealthPlanList(APIView):
	"""
	Get available health plans
	"""
	def get(self, request, format=None):
		health_plans = HealthPlan.objects.all()
		serializer = HealthPlanSerializer(health_plans, many=True)
		return Response({'message': 'Get available health plans', 'data': serializer.data})

	def get_health_plan_id(health_plan_id):
		try:
			return HealthPlan.objects.get(pk=health_plan_id)
		except HealthPlan.DoesNotExist:
			raise NotFound(detail='Health plan not found', code=status.HTTP_404_NOT_FOUND)