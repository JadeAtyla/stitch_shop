# your_app_name/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
# Corrected import path based on your directory structure
# Categories and Products models are in the 'api' app's models.py
from api.models import Categories, Products

class Command(BaseCommand):
    help = 'Seeds the database with initial categories and product data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        # Clear existing data to prevent duplicates on successive runs
        Products.objects.all().delete()
        Categories.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        self.stdout.write(self.style.MIGRATE_HEADING('Seeding Categories...'))

        # Data for categories
        categories_data = [
            {'name': 'Sewing Supplies', 'description': 'Essential items for all your sewing needs, from needles to thread.', 'parent': None},
            {'name': 'Tailoring Tools', 'description': 'Professional tools for precise cutting, measuring, and marking in tailoring.', 'parent': None},
            {'name': 'Fabrics', 'description': 'A wide selection of fabrics for various projects, including cotton, linen, and denim.', 'parent': None},
            {'name': 'Notions & Accessories', 'description': 'Small but essential items like zippers, buttons, and elastic bands to complete your sewing projects.', 'parent': None},
            {'name': 'Embroidery Supplies', 'description': 'Everything you need for beautiful embroidery, including hoops, floss, and kits.', 'parent': None},
            {'name': 'Sewing Kits & Sets', 'description': 'Convenient and comprehensive kits for beginners and for on-the-go mending.', 'parent': None},
        ]

        # Create main categories first
        created_categories = {}
        with transaction.atomic():
            for cat_data in categories_data:
                category = Categories.objects.create(
                    name=cat_data['name'],
                    description=cat_data['description'],
                    parent_category=None, # Set parent later for subcategories
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )
                created_categories[category.name] = category
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

            # Add subcategory 'Cotton Blends' linked to 'Fabrics'
            if 'Fabrics' in created_categories:
                cotton_blends = Categories.objects.create(
                    name='Cotton Blends',
                    description='Various blends of cotton fabric, a subcategory of Fabrics.',
                    parent_category=created_categories['Fabrics'],
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )
                created_categories[cotton_blends.name] = cotton_blends
                self.stdout.write(self.style.SUCCESS(f'Created subcategory: {cotton_blends.name}'))


        self.stdout.write(self.style.MIGRATE_HEADING('\nSeeding Products...'))

        # Data for products
        products_data = [
            # Sewing Supplies (category_id = 1)
            {'name': 'Sewing Needles (assorted sizes)', 'description': 'A pack of assorted sewing needles for various fabric types and hand-sewing tasks.', 'price': 5.99, 'sku': 'SSN001', 'stock_quantity': 100, 'category_name': 'Sewing Supplies', 'is_available': True, 'discount': 50.0},
            {'name': 'Spools of Thread (various colors)', 'description': 'A set of high-quality polyester thread spools in a variety of vibrant colors.', 'price': 12.50, 'sku': 'SST001', 'stock_quantity': 150, 'category_name': 'Sewing Supplies', 'is_available': True, 'discount': 30.0},
            {'name': 'Seam Rippers', 'description': 'Ergonomic seam rippers for easily removing stitches without damaging fabric.', 'price': 3.25, 'sku': 'SSR001', 'stock_quantity': 75, 'category_name': 'Sewing Supplies', 'is_available': True, 'discount': 50.0},
            {'name': 'Thimbles', 'description': 'Protective thimbles for comfortable and safe hand-sewing.', 'price': 2.00, 'sku': 'SSTH001', 'stock_quantity': 80, 'category_name': 'Sewing Supplies', 'is_available': True, 'discount': 20.0},
            {'name': 'Needle Threaders', 'description': 'Handy needle threaders to simplify threading needles.', 'price': 1.50, 'sku': 'SSNT001', 'stock_quantity': 120, 'category_name': 'Sewing Supplies', 'is_available': True, 'discount': 50.0},

            # Tailoring Tools (category_id = 2)
            {'name': 'Fabric Scissors', 'description': 'Sharp, durable fabric scissors for clean and precise cuts.', 'price': 18.99, 'sku': 'TTFS001', 'stock_quantity': 60, 'category_name': 'Tailoring Tools', 'is_available': True, 'discount': 0.0},
            {'name': 'Measuring Tapes', 'description': 'Flexible measuring tapes for accurate body and fabric measurements.', 'price': 4.50, 'sku': 'TTMT001', 'stock_quantity': 90, 'category_name': 'Tailoring Tools', 'is_available': True, 'discount': 0.0},
            {'name': 'Tailor’s Chalk', 'description': 'Assorted colors of tailor’s chalk for temporary fabric markings.', 'price': 6.75, 'sku': 'TTTC001', 'stock_quantity': 110, 'category_name': 'Tailoring Tools', 'is_available': True, 'discount': 0.0},
            {'name': 'Dressmaker Pins', 'description': 'Box of rust-proof dressmaker pins for holding fabric pieces together.', 'price': 4.00, 'sku': 'TTDP001', 'stock_quantity': 130, 'category_name': 'Tailoring Tools', 'is_available': True, 'discount': 0.0},
            {'name': 'Rotary Cutters', 'description': 'Precision rotary cutters for fast and accurate fabric cutting, especially with cutting mats.', 'price': 25.00, 'sku': 'TTRC001', 'stock_quantity': 40, 'category_name': 'Tailoring Tools', 'is_available': True, 'discount': 0.0},

            # Fabrics (category_id = 3)
            {'name': 'Cotton Fabric', 'description': 'Soft, breathable 100% cotton fabric, ideal for clothing and crafts (per yard).', 'price': 7.99, 'sku': 'FBF001', 'stock_quantity': 200, 'category_name': 'Fabrics', 'is_available': True, 'discount': 0.0},
            {'name': 'Linen Fabric', 'description': 'Natural, durable linen fabric with a beautiful drape (per yard).', 'price': 10.50, 'sku': 'FBL001', 'stock_quantity': 180, 'category_name': 'Fabrics', 'is_available': True, 'discount': 0.0},
            {'name': 'Denim', 'description': 'Sturdy denim fabric, perfect for jeans, jackets, and bags (per yard).', 'price': 14.00, 'sku': 'FBD001', 'stock_quantity': 150, 'category_name': 'Fabrics', 'is_available': True, 'discount': 0.0},
            {'name': 'Silk Blend', 'description': 'Luxurious silk blend fabric for elegant garments (per yard).', 'price': 22.00, 'sku': 'FBSB001', 'stock_quantity': 90, 'category_name': 'Fabrics', 'is_available': True, 'discount': 0.0},
            {'name': 'Polyester', 'description': 'Versatile and wrinkle-resistant polyester fabric (per yard).', 'price': 6.50, 'sku': 'FBPL001', 'stock_quantity': 250, 'category_name': 'Fabrics', 'is_available': True, 'discount': 0.0},
            {'name': 'Fleece', 'description': 'Warm and cozy fleece fabric, great for blankets and activewear (per yard).', 'price': 9.00, 'sku': 'FBF002', 'stock_quantity': 170, 'category_name': 'Fabrics', 'is_available': True, 'discount': 0.0},
            {'name': 'Printed Fabric', 'description': 'Assorted printed fabrics with various patterns and designs (per yard).', 'price': 8.50, 'sku': 'FBPR001', 'stock_quantity': 220, 'category_name': 'Fabrics', 'is_available': True, 'discount': 0.0},

            # Notions & Accessories (category_id = 4)
            {'name': 'Zippers (various sizes and types)', 'description': 'Assortment of zippers in different lengths and styles for various projects.', 'price': 7.00, 'sku': 'NAZP001', 'stock_quantity': 100, 'category_name': 'Notions & Accessories', 'is_available': True, 'discount': 0.0},
            {'name': 'Buttons (plastic, wood, metal)', 'description': 'Mixed pack of buttons in various materials, sizes, and colors.', 'price': 9.50, 'sku': 'NABT001', 'stock_quantity': 110, 'category_name': 'Notions & Accessories', 'is_available': True, 'discount': 0.0},
            {'name': 'Elastic Bands', 'description': 'Rolls of high-quality elastic bands for waistbands and cuffs.', 'price': 5.25, 'sku': 'NAEB001', 'stock_quantity': 140, 'category_name': 'Notions & Accessories', 'is_available': True, 'discount': 0.0},
            {'name': 'Hook and Eye Sets', 'description': 'Small hook and eye fasteners for closures on garments and accessories.', 'price': 3.00, 'sku': 'NAHE001', 'stock_quantity': 160, 'category_name': 'Notions & Accessories', 'is_available': True, 'discount': 0.0},
            {'name': 'Velcro Strips', 'description': 'Self-adhesive Velcro strips for easy and secure closures.', 'price': 6.00, 'sku': 'NAVS001', 'stock_quantity': 95, 'category_name': 'Notions & Accessories', 'is_available': True, 'discount': 0.0},
            {'name': 'Bias Tape', 'description': 'Rolls of pre-folded bias tape for finishing raw edges and decorative trim.', 'price': 4.75, 'sku': 'NABT002', 'stock_quantity': 120, 'category_name': 'Notions & Accessories', 'is_available': True, 'discount': 0.0},
            {'name': 'Interfacing', 'description': 'Fusible and sew-in interfacing to add structure and stability to fabrics (per yard).', 'price': 11.00, 'sku': 'NAIF001', 'stock_quantity': 80, 'category_name': 'Notions & Accessories', 'is_available': True, 'discount': 0.0},

            # Embroidery Supplies (category_id = 5)
            {'name': 'Embroidery Hoops', 'description': 'Wooden and plastic embroidery hoops in various sizes.', 'price': 8.00, 'sku': 'ESEH001', 'stock_quantity': 70, 'category_name': 'Embroidery Supplies', 'is_available': True, 'discount': 0.0},
            {'name': 'Embroidery Floss', 'description': 'Pack of assorted embroidery floss in a wide range of colors.', 'price': 15.00, 'sku': 'ESEF001', 'stock_quantity': 100, 'category_name': 'Embroidery Supplies', 'is_available': True, 'discount': 0.0},
            {'name': 'Cross-Stitch Kits', 'description': 'Beginner-friendly cross-stitch kits with patterns, fabric, and floss.', 'price': 20.00, 'sku': 'ESCK001', 'stock_quantity': 50, 'category_name': 'Embroidery Supplies', 'is_available': True, 'discount': 0.0},
            {'name': 'Fabric Marking Pens', 'description': 'Water-erasable fabric marking pens for temporary design transfers.', 'price': 6.00, 'sku': 'ESFMP001', 'stock_quantity': 85, 'category_name': 'Embroidery Supplies', 'is_available': True, 'discount': 0.0},

            # Sewing Kits & Sets (category_id = 6)
            {'name': 'Beginner Sewing Kits', 'description': 'Comprehensive kits for new sewers, including essential tools and basic notions.', 'price': 35.00, 'sku': 'SKSBK001', 'stock_quantity': 30, 'category_name': 'Sewing Kits & Sets', 'is_available': True, 'discount': 0.0},
            {'name': 'Emergency Mending Kits', 'description': 'Compact kits for quick repairs on the go.', 'price': 10.00, 'sku': 'SKSEMK001', 'stock_quantity': 60, 'category_name': 'Sewing Kits & Sets', 'is_available': True, 'discount': 0.0},
            {'name': 'Travel Sewing Kits', 'description': 'Portable sewing kits with mini essentials for travel.', 'price': 15.00, 'sku': 'SKSTSK001', 'stock_quantity': 45, 'category_name': 'Sewing Kits & Sets', 'is_available': True, 'discount': 0.0},
        ]

        with transaction.atomic():
            for prod_data in products_data:
                try:
                    category = created_categories.get(prod_data['category_name'])
                    if not category:
                        self.stdout.write(self.style.ERROR(f"Category '{prod_data['category_name']}' not found for product '{prod_data['name']}'. Skipping."))
                        continue

                    product = Products.objects.create(
                        name=prod_data['name'],
                        description=prod_data['description'],
                        price=prod_data['price'],
                        sku=prod_data['sku'],
                        stock_quantity=prod_data['stock_quantity'],
                        category=category,
                        is_available=prod_data['is_available'],
                        discount=prod_data['discount'],
                        created_at=timezone.now(),
                        updated_at=timezone.now()
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created product: {product.name} (Category: {category.name})'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating product '{prod_data['name']}': {e}"))

        self.stdout.write(self.style.SUCCESS('\nDatabase seeding complete!'))

