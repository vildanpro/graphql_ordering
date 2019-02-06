from graphene import ObjectType, String, Int, List, Argument, Schema, Date, Float
from .db import MSqlDBLoader as Sql
from .db import get_supplers, get_services, get_periods, get_periods_by_owner, get_order_data


class SuppliersObject(ObjectType):
    i_owner = Int()
    supplier = String()


class ServicesObject(ObjectType):
    cod_u = Int()
    servicename = String()


class PeriodsObject(ObjectType):
    for_period = Date()


class PeriodsByOwnerObject(ObjectType):
    for_period = Date()


class SMoneyObject(ObjectType):
    typerec = Int()
    s_money = Float()


class OrderDataObject(ObjectType):
    cod_pl = Int()
    for_period = Date()
    i_owner = Int()
    supplier = String()
    cod_u = Int()
    servicename = String()
    s_money = List(SMoneyObject)


class RangesOfPeriods(ObjectType):
    range_periods = String()


class Query(ObjectType):
    suppliers = List(SuppliersObject, cod_pl=Argument(Int))
    services = List(ServicesObject, cod_pl=Argument(Int))
    periods = List(PeriodsObject, cod_pl=Argument(Int))
    periods_by_owner = List(PeriodsByOwnerObject, i_owner=Argument(Int), cod_pl=Argument(Int))
    order_data = List(OrderDataObject, i_owner=Argument(Int), cod_pl=Argument(Int), range_of_periods=Argument(String))

    def resolve_suppliers(self, info, cod_pl=None):
        if not Sql().query_data(cod_pl):
            return Sql().query_data(cod_pl)
        else:
            suppliers = [item['_id'] for item in get_supplers(cod_pl)]
            suppliers_as_obj_list = []
            for item in suppliers:
                supplier = SuppliersObject(item['i_owner'], item['supplier'])
                suppliers_as_obj_list.append(supplier)
            return suppliers_as_obj_list

    def resolve_services(self, info, cod_pl=None):
        if not Sql().query_data(cod_pl):
            return Sql().query_data(cod_pl)
        else:
            services = [item['_id'] for item in get_services(cod_pl)]
            services_as_obj_list = []
            for item in services:
                service = ServicesObject(item['cod_u'], item['servicename'])
                services_as_obj_list.append(service)
            return services_as_obj_list

    def resolve_periods(self, info, cod_pl=None):
        if not Sql().query_data(cod_pl):
            return Sql().query_data(cod_pl)
        else:
            periods = [item['_id'] for item in get_periods(cod_pl)]
            periods_as_obj_list = []
            for item in periods:
                period = PeriodsObject(item['for_period'])
                periods_as_obj_list.append(period)
            return periods_as_obj_list

    def resolve_periods_by_owner(self, info, i_owner=None, cod_pl=None):
        if not Sql().query_data(cod_pl):
            return Sql().query_data(cod_pl)
        else:
            periods = get_periods_by_owner(i_owner=i_owner, cod_pl=cod_pl)
            periods_as_obj_list = []
            for item in periods:
                period = PeriodsByOwnerObject(item)
                periods_as_obj_list.append(period)
            return periods_as_obj_list

    def resolve_order_data(self, info, cod_pl=None, i_owner=None):
        order_data = get_order_data(cod_pl=cod_pl, i_owner=i_owner)
        order_data_as_obj_list = []
        for item in order_data:
            s_money_obj_list = [SMoneyObject(typerec=i['typerec'], s_money=i['s_money']) for i in item['s_money']]
            order_data_entry = OrderDataObject(cod_pl=item['cod_pl'],
                                               for_period=item['for_period'],
                                               i_owner=item['i_owner'],
                                               supplier=item['supplier'],
                                               cod_u=item['cod_u'],
                                               servicename=item['servicename'],
                                               s_money=s_money_obj_list)
            order_data_as_obj_list.append(order_data_entry)
        return order_data_as_obj_list


schema = Schema(query=Query, auto_camelcase=False)

