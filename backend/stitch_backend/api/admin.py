from django.contrib import admin
from .models import (
    AppUser,
    Address,
    Categories,
    Products,
    ShoppingCarts,
    CartItems,
    Payments,
    Orders,
    OrderItems
)

admin.site.register(AppUser)
admin.site.register(Address)
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(ShoppingCarts)
admin.site.register(CartItems)
admin.site.register(Payments)
admin.site.register(Orders)
admin.site.register(OrderItems)