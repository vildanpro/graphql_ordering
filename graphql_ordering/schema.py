import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from .models import Money as MoneyModel


class Money(MongoengineObjectType):
    class Meta:
        model = MoneyModel
        interfaces = (Node,)


class Query(graphene.ObjectType):
    node = Node.Field()
    money = MongoengineConnectionField(Money)


schema = graphene.Schema(query=Query, types=[Money], auto_camelcase=False)
