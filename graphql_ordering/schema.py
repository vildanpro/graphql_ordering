from graphene import ObjectType, String, Int, List, Argument, Schema, Date, Float
from .db import DataLoader as Dl


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


class OrderDataObject(ObjectType):
    cod_pl = Int()
    for_period = Date()
    i_owner = Int()
    supplier = String()
    cod_u = Int()
    servicename = String()
    typerec1 = Float()
    typerec2 = Float()
    typerec3 = Float()
    typerec4 = Float()
    typerec5 = Float()
    typerec6 = Float()
    typerec7 = Float()
    typerec8 = Float()
    typerec9 = Float()


class RangesOfPeriods(ObjectType):
    range_periods = String()


class Query(ObjectType):
    suppliers = List(SuppliersObject, cod_pl=Argument(Int))
    services = List(ServicesObject, cod_pl=Argument(Int))
    periods = List(PeriodsObject, cod_pl=Argument(Int))
    periods_by_owner = List(PeriodsByOwnerObject, i_owner=Argument(Int), cod_pl=Argument(Int))
    order_data = List(OrderDataObject, i_owner=Argument(Int), cod_pl=Argument(Int), range_of_periods=Argument(String))

    def resolve_suppliers(self, info, cod_pl=None):
        data = Dl().get_suppliers(cod_pl)
        if data:
            data_list = [item['_id'] for item in data]
            data_as_obj_list = []
            for item in data_list:
                supplier_obj = SuppliersObject(item['i_owner'], item['supplier'])
                data_as_obj_list.append(supplier_obj)
            return data_as_obj_list

    def resolve_services(self, info, cod_pl=None):
        data = Dl().get_services(cod_pl)
        if data:
            data_list = [item['_id'] for item in data]
            data_as_obj_list = []
            for item in data_list:
                service_obj = ServicesObject(item['cod_u'], item['servicename'])
                data_as_obj_list.append(service_obj)
            return data_as_obj_list

    def resolve_periods(self, info, cod_pl=None):
        data = Dl().get_periods(cod_pl)
        if data:
            data_list = [item['_id'] for item in data]
            data_as_obj_list = []
            for item in data_list:
                period_obj = PeriodsObject(item['for_period'])
                data_as_obj_list.append(period_obj)
            return data_as_obj_list

    def resolve_periods_by_owner(self, info, i_owner=None, cod_pl=None):
        data = Dl().get_periods_by_owner(cod_pl, i_owner)
        if data:
            data_as_obj_list = []
            for item in data:
                period_obj = PeriodsByOwnerObject(item)
                data_as_obj_list.append(period_obj)
            return data_as_obj_list

    def resolve_order_data(self, info, cod_pl=None, i_owner=None):
        data = Dl().get_order_data(cod_pl=cod_pl, i_owner=i_owner)
        if data:
            data_as_obj_list = []
            for item in data:
                order_obj = OrderDataObject(cod_pl=item['cod_pl'],
                                            for_period=item['for_period'],
                                            i_owner=item['i_owner'],
                                            supplier=item['supplier'],
                                            cod_u=item['cod_u'],
                                            servicename=item['servicename'],
                                            typerec1=item['typerec1'],
                                            typerec2=item['typerec2'],
                                            typerec3=item['typerec3'],
                                            typerec4=item['typerec4'],
                                            typerec5=item['typerec5'],
                                            typerec6=item['typerec6'],
                                            typerec7=item['typerec7'],
                                            typerec8=item['typerec8'],
                                            typerec9=item['typerec9'])
                data_as_obj_list.append(order_obj)
            return data_as_obj_list


schema = Schema(query=Query, auto_camelcase=False)
