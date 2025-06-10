# stitch_backend/products/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter # Import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend # Import DjangoFilterBackend

from .serializers import (
    UserSerializer, AppUserSerializer, CategoriesSerializer, AddressSerializer,
    ShoppingCartsSerializer, ProductsSerializer, OrdersSerializer,
    PaymentsSerializer, CartItemsSerializer, OrderItemsSerializer
)
from .models import (
    AppUser, Categories, Address, ShoppingCarts, Products,
    Orders, Payments, CartItems, OrderItems
)
from .filters import ( # NEW: Import all your filter classes
    AppUserFilter, CategoryFilter, ProductFilter, OrderFilter,
    CartItemFilter, AddressFilter, PaymentFilter, OrderItemFilter
)


# Custom Permissions (Remains the same)
class IsOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if isinstance(obj, AppUser):
            return obj.user == request.user
        if hasattr(obj, 'user') and hasattr(obj.user, 'user'):
            return obj.user.user == request.user
        if hasattr(obj, 'cart') and hasattr(obj.cart.user, 'user'): # For CartItems
            return obj.cart.user.user == request.user
        if hasattr(obj, 'order') and hasattr(obj.order.user, 'user'): # For OrderItems
            return obj.order.user.user == request.user
        return False


# Auth Views (Remains the same)
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# AppUser Views
class AppUserListCreate(generics.ListCreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [IsAdminUser] # Only admins can list all
    filter_backends = [DjangoFilterBackend, SearchFilter] # NEW
    filterset_class = AppUserFilter # NEW
    search_fields = ['user__username', 'user__email', 'first_name', 'last_name', 'phone'] # NEW

class AppUserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    lookup_field = 'user'
    permission_classes = [IsOwnerOrAdmin]


# Categories Views
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter] # NEW
    filterset_class = CategoryFilter # NEW
    search_fields = ['name', 'description'] # NEW

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'category_id'
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]


# Address Views
class AddressListCreate(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter] # NEW
    filterset_class = AddressFilter # NEW
    search_fields = ['street_name', 'barangay', 'city_municipality', 'province', 'postal_code'] # NEW

    def get_queryset(self):
        try:
            app_user = self.request.user.appuser
            return Address.objects.filter(user=app_user)
        except AppUser.DoesNotExist:
            return Address.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.appuser)

class AddressRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'address_id'
    permission_classes = [IsOwnerOrAdmin]


# ShoppingCart Views
class ShoppingCartListCreate(generics.ListCreateAPIView):
    serializer_class = ShoppingCartsSerializer
    permission_classes = [IsAuthenticated]
    # No filters/search here typically as it's a one-to-one with user

    def get_queryset(self):
        try:
            app_user = self.request.user.appuser
            return ShoppingCarts.objects.filter(user=app_user)
        except AppUser.DoesNotExist:
            return ShoppingCarts.objects.none()

    def perform_create(self, serializer):
        try:
            app_user = self.request.user.appuser
            if ShoppingCarts.objects.filter(user=app_user).exists():
                raise generics.ValidationError("User already has a shopping cart.")
            serializer.save(user=app_user)
        except AppUser.DoesNotExist:
            raise generics.ValidationError("AppUser profile not found for this user.")

class ShoppingCartRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingCarts.objects.all()
    serializer_class = ShoppingCartsSerializer
    lookup_field = 'cart_id'
    permission_classes = [IsOwnerOrAdmin]


# Product Views
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter] # NEW
    filterset_class = ProductFilter # NEW
    search_fields = ['name', 'description', 'sku', 'category__name'] # NEW

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = 'product_id'
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]


# Order Views
class OrderListCreate(generics.ListCreateAPIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend] # NEW: SearchFilter not as relevant for orders
    filterset_class = OrderFilter # NEW

    def get_queryset(self):
        try:
            app_user = self.request.user.appuser
            return Orders.objects.filter(user=app_user)
        except AppUser.DoesNotExist:
            return Orders.objects.none()

    def perform_create(self, serializer):
        try:
            app_user = self.request.user.appuser
            serializer.save(user=app_user)
        except AppUser.DoesNotExist:
            raise generics.ValidationError("AppUser profile not found for this user.")

class OrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    lookup_field = 'order_id'
    permission_classes = [IsOwnerOrAdmin]


# Payment Views
class PaymentListCreate(generics.ListCreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend] # NEW
    filterset_class = PaymentFilter # NEW
    # SearchFilter less useful for payments unless on transaction_id

class PaymentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    lookup_field = 'payment_id'
    permission_classes = [IsAdminUser]


# CartItem Views
class CartItemListCreate(generics.ListCreateAPIView):
    serializer_class = CartItemsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter] # NEW
    filterset_class = CartItemFilter # NEW
    search_fields = ['product__name'] # NEW

    def get_queryset(self):
        try:
            app_user = self.request.user.appuser
            cart = ShoppingCarts.objects.get(user=app_user)
            return CartItems.objects.filter(cart=cart)
        except (AppUser.DoesNotExist, ShoppingCarts.DoesNotExist):
            return CartItems.objects.none()

    def perform_create(self, serializer):
        try:
            app_user = self.request.user.appuser
            cart, created = ShoppingCarts.objects.get_or_create(user=app_user)
            serializer.save(cart=cart)
        except AppUser.DoesNotExist:
            raise generics.ValidationError("AppUser profile not found for this user.")


class CartItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItems.objects.all()
    serializer_class = CartItemsSerializer
    lookup_field = 'cart_item_id'
    permission_classes = [IsOwnerOrAdmin]

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated and not (self.request.user.is_superuser or self.request.user.is_staff):
            if obj.cart.user.user != self.request.user:
                self.permission_denied(self.request, message="You do not have permission to access this cart item.")
        return obj


# OrderItem Views
class OrderItemListCreate(generics.ListCreateAPIView):
    serializer_class = OrderItemsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter] # NEW
    filterset_class = OrderItemFilter # NEW
    search_fields = ['product__name'] # NEW

    def get_queryset(self):
        try:
            app_user = self.request.user.appuser
            user_orders = Orders.objects.filter(user=app_user)
            return OrderItems.objects.filter(order__in=user_orders)
        except AppUser.DoesNotExist:
            return OrderItems.objects.none()


class OrderItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    lookup_field = 'order_item_id'
    permission_classes = [IsOwnerOrAdmin]

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated and not (self.request.user.is_superuser or self.request.user.is_staff):
            if obj.order.user.user != self.request.user:
                self.permission_denied(self.request, message="You do not have permission to access this order item.")
        return obj