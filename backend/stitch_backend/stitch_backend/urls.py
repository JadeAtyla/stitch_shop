# stitch_backend/stitch_backend/urls.py
"""
URL configuration for stitch_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from api.views import (
    CreateUserView,
    AppUserListCreate, AppUserRetrieveUpdateDestroy,
    CategoryListCreate, CategoryRetrieveUpdateDestroy,
    AddressListCreate, AddressRetrieveUpdateDestroy,
    ShoppingCartListCreate, ShoppingCartRetrieveUpdateDestroy,
    ProductListCreate, ProductRetrieveUpdateDestroy,
    OrderListCreate, OrderRetrieveUpdateDestroy,
    PaymentListCreate, PaymentRetrieveUpdateDestroy,
    CartItemListCreate, CartItemRetrieveUpdateDestroy,
    OrderItemListCreate, OrderItemRetrieveUpdateDestroy,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication
    path("api/auth/register/", CreateUserView.as_view(), name="register"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),

    # API Endpoints for your models within the 'products' app namespace
    path("api/appusers/", AppUserListCreate.as_view(), name="appuser-list-create"),
    path("api/appusers/<int:user>/", AppUserRetrieveUpdateDestroy.as_view(), name="appuser-detail"),

    path("api/categories/", CategoryListCreate.as_view(), name="category-list-create"),
    path("products/api/categories/<int:category_id>/", CategoryRetrieveUpdateDestroy.as_view(), name="category-detail"),

    path("api/addresses/", AddressListCreate.as_view(), name="address-list-create"),
    path("api/addresses/<int:address_id>/", AddressRetrieveUpdateDestroy.as_view(), name="address-detail"),

    path("api/shoppingcarts/", ShoppingCartListCreate.as_view(), name="shoppingcart-list-create"),
    path("api/shoppingcarts/<int:cart_id>/", ShoppingCartRetrieveUpdateDestroy.as_view(), name="shoppingcart-detail"),

    path("api/products/", ProductListCreate.as_view(), name="product-list-create"),
    path("api/products/<int:product_id>/", ProductRetrieveUpdateDestroy.as_view(), name="product-detail"),

    path("api/orders/", OrderListCreate.as_view(), name="order-list-create"),
    path("api/orders/<int:order_id>/", OrderRetrieveUpdateDestroy.as_view(), name="order-detail"),

    path("api/payments/", PaymentListCreate.as_view(), name="payment-list-create"),
    path("api/payments/<int:payment_id>/", PaymentRetrieveUpdateDestroy.as_view(), name="payment-detail"),

    path("api/cartitems/", CartItemListCreate.as_view(), name="cartitem-list-create"),
    path("api/cartitems/<int:cart_item_id>/", CartItemRetrieveUpdateDestroy.as_view(), name="cartitem-detail"),

    path("api/orderitems/", OrderItemListCreate.as_view(), name="orderitem-list-create"),
    path("api/orderitems/<int:order_item_id>/", OrderItemRetrieveUpdateDestroy.as_view(), name="orderitem-detail"),
]