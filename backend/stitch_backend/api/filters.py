# stitch_backend/products/filters.py
import django_filters

from .models import (
    AppUser,
    Categories,
    Products,
    Orders,
    ShoppingCarts, # Make sure ShoppingCarts is imported for ShoppingCartFilter and CartItems
    CartItems,
    Address,
    Payments,
    OrderItems,
    UserRole,
    OrderStatus,
    AddressType,   # Corrected import for AddressType
    PaymentMethod, # Corrected import for PaymentMethod
    PaymentStatus  # Corrected import for PaymentStatus
)

# Filter for AppUser
class AppUserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    role = django_filters.ChoiceFilter(choices=UserRole.choices)
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = AppUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'created_at']

# Filter for Categories
class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    parent_category_id = django_filters.NumberFilter(field_name='parent_category__category_id') # Filter by parent ID

    class Meta:
        model = Categories
        fields = ['name', 'parent_category', 'description']

# Filter for Products
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category_id = django_filters.NumberFilter(field_name="category__category_id") # Filter by category ID
    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains') # Filter by category name
    is_available = django_filters.BooleanFilter(field_name="is_available")
    stock_quantity_gte = django_filters.NumberFilter(field_name="stock_quantity", lookup_expr='gte')

    class Meta:
        model = Products
        fields = ['name', 'price', 'category', 'is_available', 'stock_quantity']

# Filter for Orders
class OrderFilter(django_filters.FilterSet):
    user_username = django_filters.CharFilter(field_name='user__user__username', lookup_expr='icontains')
    total_amount_gte = django_filters.NumberFilter(field_name="total_amount", lookup_expr='gte')
    total_amount_lte = django_filters.NumberFilter(field_name="total_amount", lookup_expr='lte')
    order_status = django_filters.ChoiceFilter(choices=OrderStatus.choices) # Corrected
    order_date_gte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='gte')
    order_date_lte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='lte')

    class Meta:
        model = Orders
        fields = ['user', 'total_amount', 'order_status', 'order_date']

# Filter for CartItems
class CartItemFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    quantity_gte = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    quantity_lte = django_filters.NumberFilter(field_name='quantity', lookup_expr='lte')

    class Meta:
        model = CartItems
        fields = ['cart', 'product', 'quantity']

# Filter for Addresses
class AddressFilter(django_filters.FilterSet):
    user_username = django_filters.CharFilter(field_name='user__user__username', lookup_expr='icontains')
    city_municipality = django_filters.CharFilter(lookup_expr='icontains')
    province = django_filters.CharFilter(lookup_expr='icontains')
    address_type = django_filters.ChoiceFilter(choices=AddressType.choices) # Corrected

    class Meta:
        model = Address
        fields = ['user', 'city_municipality', 'province', 'address_type']

# Filter for Payments
class PaymentFilter(django_filters.FilterSet):
    order_id = django_filters.NumberFilter(field_name='order__order_id')
    payment_method = django_filters.ChoiceFilter(choices=PaymentMethod.choices) # Corrected
    payment_status = django_filters.ChoiceFilter(choices=PaymentStatus.choices) # Corrected
    amount_gte = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_lte = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    paid_at_gte = django_filters.DateTimeFilter(field_name='paid_at', lookup_expr='gte')
    paid_at_lte = django_filters.DateTimeFilter(field_name='paid_at', lookup_expr='lte')

    class Meta:
        model = Payments
        fields = ['order', 'payment_method', 'payment_status', 'amount', 'paid_at']

# Filter for OrderItems
class OrderItemFilter(django_filters.FilterSet):
    order_id = django_filters.NumberFilter(field_name='order__order_id')
    product_name = django_filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    quantity_gte = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    quantity_lte = django_filters.NumberFilter(field_name='quantity', lookup_expr='lte')

    class Meta:
        model = OrderItems
        fields = ['order', 'product', 'quantity']