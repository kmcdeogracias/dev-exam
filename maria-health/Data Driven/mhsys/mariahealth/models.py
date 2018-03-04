from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)
    on_delete = models.DO_NOTHING

class HMOProvider(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)
    on_delete = models.DO_NOTHING

class PaymentTerm(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)
    on_delete = models.DO_NOTHING

class HealthPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    cost = models.FloatField()
    payment_terms = models.ForeignKey(PaymentTerm, on_delete=models.CASCADE)
    hmo_provider = models.ForeignKey(HMOProvider, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)

class CartItem(models.Model):
    qty = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    health_plan = models.ForeignKey(HealthPlan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True, auto_now=False)