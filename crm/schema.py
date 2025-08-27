import graphene
from graphene_django import DjangoObjectType
from crm.models import Customer, Product, Order


# ----------------------
# GraphQL Types
# ----------------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


# ----------------------
# Queries
# ----------------------
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    customer = graphene.Field(CustomerType, id=graphene.Int(required=True))
    product = graphene.Field(ProductType, id=graphene.Int(required=True))
    order = graphene.Field(OrderType, id=graphene.Int(required=True))

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()

    def resolve_customer(root, info, id):
        return Customer.objects.get(pk=id)

    def resolve_product(root, info, id):
        return Product.objects.get(pk=id)

    def resolve_order(root, info, id):
        return Order.objects.get(pk=id)


# ----------------------
# Mutations
# ----------------------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)

    customer = graphene.Field(CustomerType)

    @classmethod
    def mutate(cls, root, info, name, email, phone):
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, customer_id, product_id, quantity):
        customer = Customer.objects.get(pk=customer_id)
        product = Product.objects.get(pk=product_id)
        order = Order(customer=customer, product=product, quantity=quantity)
        order.save()
        return CreateOrder(order=order)


class UpdateLowStockProducts(graphene.Mutation):
    """
    Mutation to automatically mark products as low stock if quantity < 5
    """

    updated_count = graphene.Int()

    @classmethod
    def mutate(cls, root, info):
        low_stock_products = Product.objects.filter(quantity__lt=5)
        updated_count = low_stock_products.count()

        for product in low_stock_products:
            product.low_stock = True
            product.save()

        return UpdateLowStockProducts(updated_count=updated_count)


# ----------------------
# Root Mutation
# ----------------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()


# ----------------------
# Final Schema
# ----------------------
schema = graphene.Schema(query=Query, mutation=Mutation)
