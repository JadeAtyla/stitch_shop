# stitch_backend/products/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    AppUser, Categories, Address, ShoppingCarts, Products,
    Orders, Payments, CartItems, OrderItems,
    UserRole, AddressType, PaymentMethod, PaymentStatus, OrderStatus
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AppUserSerializer(serializers.ModelSerializer):
    # The 'user' field will represent the Django User's ID
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', required=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)


    class Meta:
        model = AppUser
        # Include 'user_id', 'username', 'email' for clarity
        fields = ["user_id", "username", "email", "first_name", "middle_name", "last_name", "phone", "role", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"] # These are auto_now_add/auto_now

    # We don't need a create method here if AppUser is created after User
    # Or, if you want to create/update AppUser from this serializer,
    # you'd need to handle the nested User creation/update carefully.
    # For simplicity, I'll assume AppUser is created AFTER the Django User.


class UserSerializer(serializers.ModelSerializer):
    # Fields for Django User registration
    first_name = serializers.CharField(write_only=True, required=False)
    middle_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    role = serializers.ChoiceField(choices=UserRole.choices, read_only=True, default=UserRole.USER)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "middle_name", "last_name", "phone", "role"]
        extra_kwargs = {"password": {"write_only": True}
                        }

    def create(self, validated_data):
        # Extract AppUser specific data
        first_name = validated_data.pop('first_name', '')
        middle_name = validated_data.pop('middle_name', '')
        last_name = validated_data.pop('last_name', '')
        phone = validated_data.pop('phone', '')
        role = validated_data.pop('role', UserRole.USER)

        # Create Django User
        user = User.objects.create_user(**validated_data)

        # Create corresponding AppUser instance
        app_user = AppUser.objects.create( # Store app_user to link shopping cart
            user=user,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone=phone,
            role=role
        )

        # ALGORITHM: Create a ShoppingCart for the newly registered AppUser
        # This ensures every new user has an associated shopping cart from the start.
        ShoppingCarts.objects.create(user=app_user) # Assuming ShoppingCart model requires 'user' foreign key

        return user


class CategoriesSerializer(serializers.ModelSerializer):
    parent_category_name = serializers.CharField(source='parent_category.name', read_only=True)

    class Meta:
        model = Categories
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    # user_email = serializers.CharField(source='user.user.email', read_only=True) # Access Django User's email
    user_username = serializers.CharField(source='user.user.username', read_only=True) # Access Django User's username

    class Meta:
        model = Address
        fields = '__all__'

class ShoppingCartsSerializer(serializers.ModelSerializer):
    # user_email = serializers.CharField(source='user.user.email', read_only=True) # Access Django User's email
    # user_username = serializers.CharField(source='user.user.username', read_only=True)

    class Meta:
        model = ShoppingCarts
        fields = ["cart_id"]

class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Products
        fields = '__all__'

class PaymentsSerializer(serializers.ModelSerializer):
    order_id_display = serializers.IntegerField(source='order.order_id', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)

    class Meta:
        model = Payments
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    # user_email = serializers.CharField(source='user.user.email', read_only=True) # Access Django User's email
    user_username = serializers.CharField(source='user.user.username', read_only=True)
    shipping_address_display = serializers.CharField(source='shipping_address.__str__', read_only=True)
    billing_address_display = serializers.CharField(source='billing_address.__str__', read_only=True)
    order_status_display = serializers.CharField(source='get_order_status_display', read_only=True)
    payment_details = PaymentsSerializer(source='payment', read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'


class CartItemsSerializer(serializers.ModelSerializer):
    # Make 'cart' not required for input, as it's set by the view's perform_create
    cart = serializers.PrimaryKeyRelatedField(queryset=ShoppingCarts.objects.all(), required=False)
    cart_id_display = serializers.IntegerField(source='cart.cart_id', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItems
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    order_id_display = serializers.IntegerField(source='order.order_id', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItems
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes the TokenObtainPairSerializer to add user-specific data,
    including their shopping cart, to the token response.
    """
    def validate(self, attrs):
        # Call the parent class's validate method to get the tokens
        # This handles authentication and generates 'access' and 'refresh' tokens
        data = super().validate(attrs)

        # 'self.user' is available here after successful authentication by the parent serializer
        user = self.user

        # Retrieve the AppUser instance linked to the authenticated Django User
        try:
            app_user = AppUser.objects.get(user=user)
        except AppUser.DoesNotExist:
            raise serializers.ValidationError("AppUser profile not found for this user.")

        # Fetch the shopping cart for the app_user
        # Use .first() as filter returns a QuerySet, and we expect one cart per user
        user_cart = ShoppingCarts.objects.filter(user=app_user).first()

        # Serialize the shopping cart data if found
        if user_cart:
            cart_serializer = ShoppingCartsSerializer(user_cart)
            data['cart'] = cart_serializer.data["cart_id"]
        else:
            # Optionally, create a cart if one doesn't exist for the user on login
            # Or handle this scenario based on your business logic (e.g., return null)
            data['cart'] = None
        return data
