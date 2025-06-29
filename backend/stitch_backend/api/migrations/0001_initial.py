# Generated by Django 5.2.1 on 2025-06-10 16:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('role', models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'AppUsers',
                'db_table': 'app_user',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('street_name', models.CharField(max_length=255)),
                ('building_house_no', models.CharField(blank=True, max_length=50, null=True)),
                ('barangay', models.CharField(max_length=100)),
                ('city_municipality', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=100)),
                ('address_type', models.CharField(choices=[('shipping', 'Shipping'), ('billing', 'Billing')], default='shipping', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.appuser')),
            ],
            options={
                'verbose_name_plural': 'Addresses',
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='subcategories', to='api.categories')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Refunded', 'Refunded')], default='Pending', max_length=20)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('billing_address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='billing_orders', to='api.address')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='shipping_orders', to='api.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.appuser')),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_method', models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('GCash', 'GCash')], default='Cash On Delivery', max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed'), ('Refunded', 'Refunded')], default='Pending', max_length=20)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='api.orders')),
            ],
            options={
                'verbose_name_plural': 'Payments',
                'db_table': 'payments',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sku', models.CharField(blank=True, max_length=50, null=True)),
                ('stock_quantity', models.IntegerField(default=0)),
                ('image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('sizes', models.CharField(blank=True, max_length=255, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.categories')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('order_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('price_at_time_of_order', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orders')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.products')),
            ],
            options={
                'verbose_name_plural': 'Order Items',
                'db_table': 'order_items',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCarts',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.appuser')),
            ],
            options={
                'verbose_name_plural': 'Shopping Carts',
                'db_table': 'shopping_carts',
            },
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('cart_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.products')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.shoppingcarts')),
            ],
            options={
                'db_table': 'cart_items',
                'unique_together': {('cart', 'product')},
            },
        ),
    ]
