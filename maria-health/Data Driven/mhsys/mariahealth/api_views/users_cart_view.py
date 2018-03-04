from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from mariahealth.models import Cart, CartItem, User, HealthPlan
from mariahealth.serializers import CartSerializer, CartCreateSerializer, CartItemSerializer
from mariahealth.api_views.users_view import UserDetails
from mariahealth.api_views.cart_items_view import CartItemList
from datetime import datetime

class UserCartList(APIView):
	"""
	Get user cart, create cart, and change status to paid
	"""
	def get(self, request, user_id):
		user = UserDetails.get_user_id(user_id)
		carts = Cart.objects.filter(user=user.id, deleted_at=None)
		serializer = CartSerializer(carts, many=True)
		return Response({'message': 'Get user cart list', 'data': serializer.data})

	def post(self, request, user_id):
		user = UserDetails.get_user_id(user_id)
		
		user_params = {'user': user_id}
		serializer = CartCreateSerializer(data=user_params)

		if serializer.is_valid():
			serializer.save()
			msg, data, status_code = 'Cart created', serializer.data, status.HTTP_201_CREATED
		else:
			msg, data, status_code = 'Bad Request', serializer.errors, status.HTTP_400_BAD_REQUEST
		
		return Response({'message': msg, 'data': data}, status=status_code)

	def put(self, request, user_id, cart_id):
		user_cart = CartItemList.get_user_cart(cart_id, user_id)

		updated_at = datetime.now()
		paid = True
		params = {'paid': paid, 'updated_at': updated_at}
		serializer = CartSerializer(user_cart, data=params, partial=True)
		
		if serializer.is_valid():
			serializer.paid = True
			serializer.updated_at = updated_at
			serializer.save()
			msg, data, status_code = 'Updated user cart', serializer.data, status.HTTP_200_OK
		else:
			msg, data, status_code = 'Bad Request', serializers.errors, status.HTTP_400_BAD_REQUEST
		
		return Response({'message': msg, 'data': data}, status=status_code)