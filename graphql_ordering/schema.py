import graphene
from flask import json
from .models import Money as MoneyModel
from .database import load_data_to_mongo, get_suppliers, get_periods, get_servicenames
from pprint import pprint


class Supplier(graphene.ObjectType):
    i_owner = graphene.Int()
    supplier = graphene.String()


class Servicename(graphene.ObjectType):
    cod_u = graphene.Int()
    servicename = graphene.String()


class Periods(graphene.ObjectType):
    periods = graphene.String()


class Query(graphene.ObjectType):

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

    suppliers = graphene.List(Supplier, cod_pl=graphene.Argument(graphene.Int))

    def resolve_suppliers(self, info, cod_pl=None):
        if not MoneyModel.objects(cod_pl=cod_pl).first():
            load_data_to_mongo(cod_pl)

        suppliers = get_suppliers()
        suppliers_as_obj_list = []
        for item in suppliers:
            supplier = Supplier(item['i_owner'], item['supplier'])
            suppliers_as_obj_list.append(supplier)
        return suppliers_as_obj_list

    servicenames = graphene.List(Servicename, cod_pl=graphene.Argument(graphene.Int, required=False))

    def resolve_servicenames(self, info, cod_pl=None):
        if cod_pl:
            if MoneyModel.objects(cod_pl=cod_pl).first():
                servicenames = get_servicenames()
                servicenames_as_obj_list = []
                for item in servicenames:
                    servicename = Servicename(item['cod_u'], item['servicename'])
                    servicenames_as_obj_list.append(servicename)
                return servicenames_as_obj_list
            else:
                load_data_to_mongo(cod_pl)
                servicenames = json.dumps(get_servicenames())
                return json.loads(servicenames)

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


schema = graphene.Schema(query=Query, auto_camelcase=False)
