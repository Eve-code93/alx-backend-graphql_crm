import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter


# --------------------------
# GraphQL Types
# --------------------------

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)


# --------------------------
# Input Types
# --------------------------

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


# --------------------------
# Mutations
# --------------------------

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    customers_created = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, customers):
        created = []
        errors = []
        for data in customers:
            if Customer.objects.filter(email=data.email).exists():
                errors.append(f"Email {data.email} already exists")
                continue
            customer = Customer(name=data.name, email=data.email, phone=data.phone)
            customer.save()
            created.append(customer)
        return BulkCreateCustomers(customers_created=created, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise ValidationError("Price must be positive")
        if stock < 0:
            raise ValidationError("Stock cannot be negative")
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.String()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise ValidationError("Customer does not exist")

        products = Product.objects.filter(id__in=product_ids)
        if not products.exists():
            raise ValidationError("No valid products provided")

        order = Order(customer=customer)
        if order_date:
            order.order_date = parse_datetime(order_date)
        order.save()
        order.products.set(products)
        order.total_amount = sum(p.price for p in products)
        order.save()
        return CreateOrder(order=order)


# --------------------------
# Mutation Class
# --------------------------

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


# --------------------------
# Query Class (with filters + ordering)
# --------------------------

class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerType, order_by=graphene.List(of_type=graphene.String))
    all_products = DjangoFilterConnectionField(ProductType, order_by=graphene.List(of_type=graphene.String))
    all_orders = DjangoFilterConnectionField(OrderType, order_by=graphene.List(of_type=graphene.String))

    def resolve_all_customers(root, info, **kwargs):
        qs = Customer.objects.all()
        order_by = kwargs.get("order_by")
        return qs.order_by(*order_by) if order_by else qs

    def resolve_all_products(root, info, **kwargs):
        qs = Product.objects.all()
        order_by = kwargs.get("order_by")
        return qs.order_by(*order_by) if order_by else qs

    def resolve_all_orders(root, info, **kwargs):
        qs = Order.objects.all()
        order_by = kwargs.get("order_by")
        return qs.order_by(*order_by) if order_by else qs
