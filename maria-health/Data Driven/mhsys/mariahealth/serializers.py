from rest_framework import serializers
from mariahealth.models import User, HMOProvider, PaymentTerm, HealthPlan, Cart, CartItem

class UserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name')

class HMOProviderSerializer(serializers.ModelSerializer):
	class Meta:
		model = HMOProvider
		fields = ('id', 'name')

class PaymentTermSerializer(serializers.ModelSerializer):
	class Meta:
		model = PaymentTerm
		fields = ('id', 'name')

class HealthPlanSerializer(serializers.ModelSerializer):
	hmo_provider = HMOProviderSerializer(read_only=True)
	payment_terms = PaymentTermSerializer(read_only=True)
	class Meta:
		model = HealthPlan
		fields = ('id', 'name', 'description', 'cost', 'payment_terms', 'hmo_provider')

class CartSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Cart
		fields = ('id', 'user', 'paid', 'created_at', 'updated_at')

class CartCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cart
		fields = ('id', 'user', 'paid', 'created_at', 'updated_at')

class CartItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = ('qty', 'cart', 'health_plan', 'created_at', 'updated_at', 'deleted_at')

class CartItemGetSerializer(serializers.ModelSerializer):
	health_plan = HealthPlanSerializer(read_only=True)
	class Meta:
		model = CartItem
		fields = ('id', 'qty', 'cart', 'health_plan', 'created_at', 'updated_at')