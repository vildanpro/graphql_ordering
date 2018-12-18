import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from .models import Period as PeriodModel
from .models import Supplier as SupplierModel
from .models import Service as ServiceModel
from .models import Money as MoneyModel


class Period(MongoengineObjectType):

    class Meta:
        model = PeriodModel
        interfaces = (Node,)


class Supplier(MongoengineObjectType):

    class Meta:
        model = SupplierModel
        interfaces = (Node,)


class Service(MongoengineObjectType):

    class Meta:
        model = ServiceModel
        interfaces = (Node,)


class Money(MongoengineObjectType):

    class Meta:
        model = MoneyModel
        filter_fields = ['period']
        interfaces = (Node,)


class Query(graphene.ObjectType):

    period = graphene.String(argument=graphene.String(default_value="200"))

    def resolve_period(self, info, argument):
        return MoneyModel.objects(period=argument)

    # node = Node.Field()
    # all_money = MongoengineConnectionField(Money)
    # all_period = MongoengineConnectionField(Period)
    # all_supplier = MongoengineConnectionField(Supplier)
    # period = graphene.Field(Period)


schema = graphene.Schema(query=Query, types=[Service, Supplier, Period, Money])
