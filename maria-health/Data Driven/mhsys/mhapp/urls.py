from django.conf import settings
from django.urls import include, path
from mariahealth.views import SystemHealthChecker
from mariahealth.api_views.users_view import UserList, UserDetails
from mariahealth.api_views.users_cart_view import UserCartList
from mariahealth.api_views.cart_items_view import CartItemList
from mariahealth.api_views.health_plans_view import HealthPlanList

urlpatterns = [
    path('ruok', SystemHealthChecker.as_view()),
    
    path('health_plans', HealthPlanList.as_view()),
    
    path('users', UserList.as_view()),
    path('users/<user_id>', UserDetails.as_view()),
    
    path('users/<user_id>/carts', UserCartList.as_view()),
    path('users/<user_id>/carts/<cart_id>', UserCartList.as_view()),
    
    path('users/<user_id>/carts/<cart_id>/items', CartItemList.as_view()),
    path('users/<user_id>/carts/<cart_id>/items/<item_id>', CartItemList.as_view()),
]