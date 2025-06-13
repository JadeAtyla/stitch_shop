# stitch_backend/products/models.py
from django.db import models
from django.contrib.auth.models import User # Import Django's User model

# Define choices for ENUM fields
class UserRole(models.TextChoices):
    USER = 'user', 'User'
    ADMIN = 'admin', 'Admin'

class AddressType(models.TextChoices):
    SHIPPING = 'shipping', 'Shipping'
    BILLING = 'billing', 'Billing'

class PaymentMethod(models.TextChoices):
    CASH_ON_DELIVERY = 'Cash On Delivery', 'Cash On Delivery'
    GCASH = 'GCash', 'GCash'

class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    COMPLETED = 'Completed', 'Completed'
    FAILED = 'Failed', 'Failed'
    REFUNDED = 'Refunded', 'Refunded'

class OrderStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    PROCESSING = 'Processing', 'Processing'
    DELIVERED = 'Delivered', 'Delivered'
    CANCELLED = 'Cancelled', 'Cancelled'
    REFUNDED = 'Refunded', 'Refunded'

class AppUser(models.Model):
    # Link to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) # Changed primary_key to user

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        
        db_table = 'app_user' # Adjusted table name for clarity if needed
        verbose_name_plural = 'AppUsers'

    def __str__(self):
        return f"{self.first_name or ""} {self.last_name or ""} ({self.user.username or ""})" # Use user.username or user.email

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name or ""


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AppUser, models.CASCADE) # Link to AppUser
    street_name = models.CharField(max_length=255)
    building_house_no = models.CharField(max_length=50, blank=True, null=True)
    barangay = models.CharField(max_length=100)
    city_municipality = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    address_type = models.CharField(
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.SHIPPING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        
        db_table = 'address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.building_house_no or ""} {self.street_name or ""}, {self.barangay or ""}, {self.city_municipality or ""}, {self.province or ""}"


class ShoppingCarts(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(AppUser, models.CASCADE) # One cart per AppUser
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'shopping_carts'
        verbose_name_plural = 'Shopping Carts'

    def __str__(self):
        return f"Shopping Cart for {self.user.user.username or ""}" # Access Django User's username


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, blank=True, null=True) # Stock Keeping Unit
    stock_quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    sizes = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        
        db_table = 'products'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name or ""


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AppUser, models.CASCADE) # Link to AppUser
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    shipping_address = models.ForeignKey(Address, models.DO_NOTHING, related_name='shipping_orders')
    billing_address = models.ForeignKey(Address, models.DO_NOTHING, related_name='billing_orders')
    delivery_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        
        db_table = 'orders'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.order_id} by {self.user.user.username}"


class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Orders, models.CASCADE, related_name='payment') # One payment per order
    payment_method = models.CharField(
        max_length=50,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH_ON_DELIVERY,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        
        db_table = 'payments'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment {self.payment_id or ""} - {self.payment_status or ""} for {self.amount or ""}"


class CartItems(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(ShoppingCarts, models.CASCADE)
    product = models.ForeignKey(Products, models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        db_table = 'cart_items'
        unique_together = (('cart', 'product'),)

    def __str__(self):
        return f"{self.quantity or "0"} x {self.product.name or "0"} in Cart {self.cart.cart_id or "0"}"


class OrderItems(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, models.CASCADE)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    quantity = models.IntegerField()
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        
        db_table = 'order_items'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity or "0"} x {self.product.name or "0"} for Order {self.order.order_id or "0"}"