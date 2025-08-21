import os
import django
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql.settings")
django.setup()

from crm.models import Customer, Product, Order

# Clear old data
Customer.objects.all().delete()
Product.objects.all().delete()
Order.objects.all().delete()

# Seed Customers
customers = [
    {"name": "Alice", "email": "alice@example.com", "phone": "+1234567890"},
    {"name": "Bob", "email": "bob@example.com", "phone": "123-456-7890"},
    {"name": "Carol", "email": "carol@example.com"},
]
for c in customers:
    Customer.objects.create(**c)

# Seed Products
products = [
    {"name": "Laptop", "price": Decimal("999.99"), "stock": 10},
    {"name": "Phone", "price": Decimal("499.99"), "stock": 20},
    {"name": "Tablet", "price": Decimal("299.99"), "stock": 15},
]
for p in products:
    Product.objects.create(**p)

print("✅ Database seeded with sample customers and products!")
