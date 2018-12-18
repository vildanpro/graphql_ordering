from pprint import pprint

from mongoengine import connect
from .models import Service, Supplier, Period, Money
from .mssqldb import MSqlDBLoader
from flask import json


# connect('graphene-mongo-example', host='mongomock://localhost', alias='default')

connect('test', host='mongodb', port=27017)


def init_db(cod_pl):
    data = MSqlDBLoader().mssql_query(cod_pl)
    period_list = []
    cod_u__list = []
    i_owner_list = []
    with open('data.txt', 'w') as f:
        for i in data:
            f.write(json.dumps(i, default=str, sort_keys=True, indent=4, ensure_ascii=False))
    for i in data:
        period_field = str(i['for_period'])
        cod_u_field = str(i['cod_u'])
        servicename_field = str(i['servicename'])
        i_owner_field = str(i['i_owner'])
        supplier_field = str(i['supplier'])
        amount_field = float(i['s_money'])
        typerec_field = int(i['typerec'])

        if period_field not in period_list:
            period = Period(name=period_field)
            period.save()
            period_list.append(period_field)
            print(period_field, 'ADDED')
        else:
            period = Period.objects.get(name=period_field)

        if cod_u_field not in cod_u__list:
            servicename = Service(name=servicename_field, cod_u=cod_u_field)
            servicename.save()
            cod_u__list.append(cod_u_field)
            print(servicename_field, cod_u_field, 'ADDED')
        else:
            servicename = Service.objects.get(cod_u=cod_u_field)

        if i_owner_field not in i_owner_list:
            supplier = Supplier(name=supplier_field, i_owner=i_owner_field)
            supplier.save()
            i_owner_list.append(i_owner_field)
            print(supplier_field, i_owner_field, 'ADDED')
        else:
            supplier = Supplier.objects.get(i_owner=i_owner_field)

        money = Money(
            amount=amount_field, typerec=typerec_field, period=period, supplier=supplier,
            service=servicename
        )
        money.save()
    return json.dumps(data, default=str, sort_keys=True, indent=4, ensure_ascii=False)



