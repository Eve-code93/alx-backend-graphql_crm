import django_filters
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    created_at = django_filters.DateFromToRangeFilter()
    phone = django_filters.CharFilter(method="filter_phone")

    class Meta:
        model = Customer
        fields = ["name", "email", "created_at"]

    def filter_phone(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    price = django_filters.RangeFilter()
    stock = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = ["name", "price", "stock"]

class OrderFilter(django_filters.FilterSet):
    total_amount = django_filters.RangeFilter()
    order_date = django_filters.DateFromToRangeFilter()
    customer_name = django_filters.CharFilter(field_name="customer__name", lookup_expr="icontains")
    product_name = django_filters.CharFilter(field_name="products__name", lookup_expr="icontains")

    class Meta:
        model = Order
        fields = ["total_amount", "order_date"]
