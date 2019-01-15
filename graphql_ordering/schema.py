import graphene
from flask import json
from .models import Money as MoneyModel
from .database import load_data_to_mongo, get_suppliers, get_ranges_of_periods, get_order_data, get_owner_periods
from pprint import pprint


class Supplier(graphene.ObjectType):
    i_owner = graphene.Int()
    supplier = graphene.String()


class Servicename(graphene.ObjectType):
    cod_u = graphene.Int()
    servicename = graphene.String()


class RangesOfPeriods(graphene.ObjectType):
    range_periods = graphene.String()


class OwnerPeriods(graphene.ObjectType):
    owner_period = graphene.Int()


class Order(graphene.ObjectType):
    cod_pl = graphene.Int()
    for_period = graphene.Int()
    i_owner = graphene.Int()
    supplier = graphene.String()
    cod_u = graphene.Int()
    servicename = graphene.String()
    typerec_1 = graphene.Float()
    typerec_2 = graphene.Float()
    typerec_minus60 = graphene.Float()
    typerec_6 = graphene.Float()
    typerec_7 = graphene.Float()
    typerec_9 = graphene.Float()
    typerec_minus66 = graphene.Float()
    typerec_minus10 = graphene.Float()
    typerec_minus7 = graphene.Float()
    typerec_minus6 = graphene.Float()
    typerec_minus1 = graphene.Float()
    total = graphene.Float()


class Query(graphene.ObjectType):

    suppliers = graphene.List(Supplier, cod_pl=graphene.Argument(graphene.Int))

    def resolve_suppliers(self, info, cod_pl=None):
        if load_data_to_mongo(cod_pl):
            suppliers = get_suppliers(cod_pl)
            suppliers_as_obj_list = []
            for item in suppliers:
                supplier = Supplier(item['i_owner'], item['supplier'])
                suppliers_as_obj_list.append(supplier)
            return suppliers_as_obj_list

    ranges_of_periods = graphene.List(RangesOfPeriods,
                                      i_owner=graphene.Argument(graphene.Int),
                                      cod_pl=graphene.Argument(graphene.Int))

    def resolve_ranges_of_periods(self, info, i_owner=None, cod_pl=None):
        if load_data_to_mongo(cod_pl):
            ranges_of_periods = get_ranges_of_periods(i_owner=i_owner, cod_pl=cod_pl)
            ranges_of_periods_as_obj_list = []
            for item in ranges_of_periods:
                range_of_periods = RangesOfPeriods(item)
                ranges_of_periods_as_obj_list.append(range_of_periods)
            return ranges_of_periods_as_obj_list

    owner_periods = graphene.List(OwnerPeriods, i_owner=graphene.Argument(graphene.Int),
                                      cod_pl=graphene.Argument(graphene.Int))

    def resolve_owner_periods(self, info, i_owner=None, cod_pl=None):
        if load_data_to_mongo(cod_pl):
            owner_periods = get_owner_periods(i_owner=i_owner, cod_pl=cod_pl)
            owner_periods_as_obj_list = []
            for item in owner_periods:
                print(item)
                owner_period = OwnerPeriods(item)
                owner_periods_as_obj_list.append(owner_period)
            return owner_periods_as_obj_list

    order = graphene.List(Order,
                          i_owner=graphene.Argument(graphene.Int),
                          cod_pl=graphene.Argument(graphene.Int),
                          range_of_periods=graphene.Argument(graphene.String))

    def resolve_order(self, info, cod_pl=None, i_owner=None, range_of_periods=None):
        if load_data_to_mongo(cod_pl):
            order_data = get_order_data(cod_pl=cod_pl, i_owner=i_owner, range_of_periods=range_of_periods)
            order_data_as_obj_list = []
            for item in order_data:
                order_enty = Order(cod_pl=item['_id']['cod_pl'],
                                   for_period=item['_id']['for_period'],
                                   i_owner=item['_id']['i_owner'],
                                   supplier=item['_id']['supplier'],
                                   cod_u=item['_id']['cod_u'],
                                   servicename=item['_id']['servicename'],
                                   typerec_1=item['typerec_1'],
                                   typerec_2=item['typerec_2'],
                                   typerec_minus60=item['typerec_minus60'],
                                   typerec_6=item['typerec_6'],
                                   typerec_7=item['typerec_7'],
                                   typerec_9=item['typerec_9'],
                                   typerec_minus66=item['typerec_minus66'],
                                   typerec_minus10=item['typerec_minus10'],
                                   typerec_minus7=item['typerec_minus7'],
                                   typerec_minus6=item['typerec_minus6'],
                                   typerec_minus1=item['typerec_minus1'],
                                   total=item['total']
                                   )
                order_data_as_obj_list.append(order_enty)
            return order_data_as_obj_list


schema = graphene.Schema(query=Query, auto_camelcase=False)
