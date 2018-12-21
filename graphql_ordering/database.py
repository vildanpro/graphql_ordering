import json
from pprint import pprint
from mongoengine import connect
from .mssqldb import MSqlDBLoader as Loader
from .cluster import cluster
from .models import Money, money_schema


connect('test', host='mongodb', port=27017)


def get_data_from_mssql(cod_pl):
    return Loader().query_to_mssql(cod_pl)


def get_periods():
    data = list(set(Money.objects.distinct('for_period')))
    data_group = cluster(data, 1)
    periods = []
    for item in data_group:
        first = item[0]
        last = item[-1]
        period = str(first) + '-' + str(last)
        periods.append(period)
    return periods


def get_suppliers():
    i_owner_set = set(Money.objects.distinct('i_owner'))
    suppliers = list()
    for i_owner in i_owner_set:
        supplier = Money.objects(i_owner=i_owner).distinct('supplier')
        supplier_dict = dict()
        supplier_dict['i_owner'] = i_owner
        supplier_dict['supplier'] = supplier[0]
        suppliers.append(supplier_dict)
    return suppliers


def load_data_to_mongo(cod_pl):
    data = get_data_from_mssql(cod_pl)
    for item in data:
        d, errors = money_schema.load(item)
        d.save()



