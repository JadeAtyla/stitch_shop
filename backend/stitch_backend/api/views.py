# stitch_backend/products/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

# Revert to standard Simple JWT views that return tokens in the response body
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken # Still needed for blacklisting on logout

from django.contrib.auth import logout as django_logout # Still useful for session logout if SessionAuth is active

from django.conf import settings
SIMPLE_JWT = settings.SIMPLE_JWT # Keep loading SIMPLE_JWT for settings like BLACKLIST_AFTER_ROTATION


from .serializers import (
    UserSerializer, AppUserSerializer, CategoriesSerializer, AddressSerializer,
    ShoppingCartsSerializer, ProductsSerializer, OrdersSerializer,
    PaymentsSerializer, CartItemsSerializer, OrderItemsSerializer
)
from .models import (
    AppUser, Categories, Address, ShoppingCarts, Products,
    Orders, Payments, CartItems, OrderItems
)
from .filters import (
    AppUserFilter, CategoryFilter, ProductFilter, OrderFilter,
    CartItemFilter, AddressFilter, PaymentFilter, OrderItemFilter
)


# Custom Permissions (Remains the same)
class IsOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if isinstance(obj, AppUser):
            print("Object: ", obj.user, " Request: ")
            return obj.user == request.user
        if hasattr(obj, 'user') and hasattr(obj.user, 'user'):
            return obj.user.user == request.user
        if hasattr(obj, 'cart') and hasattr(obj.cart.user, 'user'): # For CartItems
            return obj.cart.user.user == request.user
        if hasattr(obj, 'order') and hasattr(obj.order.user, 'user'): # For OrderItems
            return obj.order.user.user == request.user
        return False

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


# Auth Views
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # User must be authenticated to logout

    def post(self, request):
        try:
            # For localStorage approach, the frontend sends the refresh token to blacklist
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            # If using Django session authentication alongside JWT
            django_logout(request)

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except (KeyError, TokenError):
            # KeyError if 'refresh' not in request.data, TokenError if token is invalid/blacklisted
            return Response({"detail": "Invalid token or already logged out."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailView(APIView):
    """
    Returns details of the currently authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        app_user = None
        user_address = []
        try:
            app_user = user.appuser # Assuming one-to-one 
            address = Address.objects.filter(user=app_user)
            user_address = AddressSerializer(address, many=True).data
        except AppUser.DoesNotExist and Address.DoesNotExist:
            pass

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email, # Django User's email
        }
        if app_user:
            data.update({
                'first_name': app_user.first_name,
                'last_name': app_user.last_name,
                'middle_name': app_user.middle_name,
                'phone': app_user.phone,
                'role': app_user.role,
                'created_at': app_user.created_at,
                'updated_at': app_user.updated_at,
                'address': user_address,
            })
        return Response(data, status=status.HTTP_200_OK)


# AppUser Views (remaining views are unchanged as they don't depend on token handling method)
class AppUserListCreate(generics.ListCreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AppUserFilter
    search_fields = ['user__username', 'user__email', 'first_name', 'last_name', 'phone']


class AppUserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    lookup_field = 'user'
    permission_classes = [IsOwnerOrAdmin]


# Categories Views
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CategoryFilter
    search_fields = ['name', 'description']

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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AddressFilter
    search_fields = ['street_name', 'barangay', 'city_municipality', 'province', 'postal_code']

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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku', 'category__name']

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

class PaymentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    lookup_field = 'payment_id'
    permission_classes = [IsAdminUser]


# CartItem Views
class CartItemListCreate(generics.ListCreateAPIView):
    serializer_class = CartItemsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CartItemFilter
    search_fields = ['product__name']


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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OrderItemFilter
    search_fields = ['product__name']


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

class ProtectedView(APIView):
    """
    A simple protected API endpoint that requires authentication.
    Returns a success message if the user is authenticated.
    """
    permission_classes = [IsAuthenticated] # Explicitly requires an authenticated user

    def get(self, request, *args, **kwargs):
        # Access the authenticated user through request.user
        user_id = request.user.id
        username = request.user.username
        return Response(
            {"message": f"Welcome, {username}! You have accessed a protected route.", "user_id": user_id},
            status=status.HTTP_200_OK
        )
