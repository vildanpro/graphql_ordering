import graphene
from pprint import pprint
from flask import json
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField


from .models import Money as MoneyModel
from .database import load_data_to_mongo, get_suppliers, get_periods


class Money(MongoengineObjectType):
    class Meta:
        model = MoneyModel
        interfaces = (Node,)


class Supplier(graphene.ObjectType):
    i_owner = graphene.Int()
    supplier = graphene.String()


class Supplier(graphene.ObjectType):
    i_owner = graphene.Int()
    supplier = graphene.String()


class Periods(graphene.ObjectType):
    periods = graphene.String()


class Query(graphene.ObjectType):
    node = Node.Field()
    money = MongoengineConnectionField(Money)

    reload_data = graphene.String(
        cod_pl=graphene.Argument(graphene.Int, required=False)
    )

    def resolve_reload_data(self, info, cod_pl=None):
        response = {
            'Old collection': None,
            'Data': None
        }
        if cod_pl:
            if MoneyModel.objects(cod_pl=cod_pl).first():
                MoneyModel.drop_collection()
                response['Old collection'] = 'Droped'
            else:
                response['Old collection'] = 'Not exist'
        load_data_to_mongo(cod_pl)
        response['Data'] = 'Loaded'
        response = json.dumps(response)
        return json.loads(response)

    suppliers = graphene.List(Supplier, cod_pl=graphene.Argument(graphene.Int, required=False))

    def resolve_suppliers(self, info, cod_pl=None):
        if cod_pl:
            if MoneyModel.objects(cod_pl=cod_pl).first():
                suppliers = get_suppliers()
                suppliers_as_obj_list = []
                for item in suppliers:
                    supplier = Supplier(item['i_owner'], item['supplier'])
                    suppliers_as_obj_list.append(supplier)
                return suppliers_as_obj_list
            else:
                load_data_to_mongo(cod_pl)
                suppliers = json.dumps(get_suppliers())
                return json.loads(suppliers)

    range_periods = graphene.String(
        start_period=graphene.Argument(graphene.Int, required=False),
        end_period=graphene.Argument(graphene.Int, required=False)
    )

    def resolve_range_periods(self, info, start_period=None, end_period=None):
        if start_period and end_period:
            periods_in_range = MoneyModel.objects(
                for_period__gt=start_period, for_period__lt=end_period).to_json()
            return json.loads(periods_in_range)

    periods = graphene.List(Periods, i_owner=graphene.Argument(graphene.Int, required=False))

    def resolve_periods(self, info, i_owner=None):
        if i_owner:
            periods = get_periods(i_owner)
            periods_obj_list = []
            for item in periods:
                period = Periods(item)
                periods_obj_list.append(period)
            return periods_obj_list


schema = graphene.Schema(query=Query, types=[Money], auto_camelcase=False)
