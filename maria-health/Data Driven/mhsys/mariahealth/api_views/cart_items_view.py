from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from mariahealth.models import Cart, CartItem, User, HealthPlan
from mariahealth.serializers import CartSerializer, CartCreateSerializer, CartItemSerializer, CartItemGetSerializer
from mariahealth.api_views.users_view import UserDetails
from mariahealth.api_views.health_plans_view import HealthPlanList
from datetime import datetime

class CartItemList(APIView):

	def get(self, request, user_id, cart_id):
		user_cart = CartItemList.get_user_cart(cart_id, user_id)
		cart_items = CartItemList.get_cart_item(user_cart)
		serializer = CartItemGetSerializer(cart_items, many=True)
		return Response({'message': 'Get cart items', 'data': serializer.data})

	def post(self, request, user_id, cart_id):
		user_cart = CartItemList.get_user_cart(cart_id, user_id)
		
		health_plan_id = request.data.get('health_plan_id', None)
		qty = request.data.get('qty', 1)

		health_plan = HealthPlanList.get_health_plan_id(health_plan_id)
		
		params = {'cart': cart_id, 'health_plan': health_plan_id, 'qty': qty}
		serializer = CartItemSerializer(data=params)

		if serializer.is_valid():
			serializer.save()
			msg, data, status_code = 'Added item to cart', serializer.data, status.HTTP_201_CREATED
		else:
			msg, data, status_code = 'Bad Request', serializer.errors, status.HTTP_400_BAD_REQUEST

		return Response({'message': msg, 'data': data}, status=status_code)

	def put(self, request, user_id, cart_id, item_id):
		user_cart = CartItemList.get_user_cart(cart_id, user_id)
		cart_item = CartItemList.get_cart_item(user_cart, item_id)

		qty = request.data.get('qty', cart_item.qty)
		updated_at = datetime.now()
		params = {'qty': qty, 'updated_at': updated_at}
		serializer = CartItemSerializer(cart_item, data=params, partial=True)
		
		if serializer.is_valid():
			serializer.qty = qty
			serializer.save()
			msg, data, status_code = 'Updated item quantity', serializer.data, status.HTTP_200_OK
		else:
			msg, data, status_code = 'Bad Request', serializer.errors, status.HTTP_400_BAD_REQUEST
		
		return Response({'message': msg, 'data': data}, status=status_code)

	def delete(self, request, user_id, cart_id, item_id):
		user_cart = CartItemList.get_user_cart(cart_id, user_id)
		cart_item = CartItemList.get_cart_item(user_cart, item_id)

		deleted_at = datetime.now()
		serializer = CartItemSerializer(cart_item, data={'deleted_at': deleted_at}, partial=True)
		
		if serializer.is_valid():
			serializer.deleted_at = deleted_at
			serializer.save()
			msg, data, status_code = 'Deleted cart item', None, status.HTTP_204_NO_CONTENT
		else:
			msg, data, status_code = 'Bad Request', serializer.errors, status.HTTP_400_BAD_REQUEST
		
		return Response({'message': msg, 'data': data}, status=status_code)

	def get_user_cart(cart_id, user_id):
		try:
			user = UserDetails.get_user_id(user_id)
			return Cart.objects.get(pk=cart_id, user=user.id, deleted_at=None)
		except Cart.DoesNotExist:
			raise NotFound(detail='User cart not found', code=status.HTTP_404_NOT_FOUND)

	def get_cart_item(user_cart, item_id=None):
		try:
			if item_id:
				return CartItem.objects.get(pk=item_id, cart=user_cart.id, deleted_at=None)
			else:
				return CartItem.objects.filter(cart=user_cart.id, deleted_at=None).all()
		except CartItem.DoesNotExist:
			raise NotFound(detail='Cart Item Not Found', code=status.HTTP_404_NOT_FOUND)
