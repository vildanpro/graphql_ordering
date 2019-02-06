from mssql import BaseDBQuery
from pymongo import MongoClient
from .utils import get_query


class DataLoader(BaseDBQuery):
    client = MongoClient('mongodb', 27017)
    # client.drop_database('order_data')
    mongodb = client.order_data

    def check_cod_pl(self, cod_pl):
        return cod_pl if isinstance(cod_pl, int) and cod_pl > 0 else 0

    def load_data_from_sql(self, cod_pl):
        cod_pl = self.check_cod_pl(cod_pl)
        query = get_query(cod_pl)
        cursor = self.call(query)

        if cursor.rowcount == 0:
            cursor.close()
            result = None
        else:
            result = cursor.fetchall()
            cursor.close()

        list_of_dicts = list()
        if result:
            for r in result:
                entry = self.to_dict(r)
                s_money_float = float(entry['s_money'])
                typerec_str = str(entry['typerec'])
                index = None
                if len(list_of_dicts) > 0:
                    for i, item in enumerate(list_of_dicts):
                        if entry['for_period'] and entry['i_owner'] and entry['cod_u'] in item.values():
                            index = i
                            break
                if index:
                    list_of_dicts[index]['typerec' + typerec_str] += s_money_float
                else:
                    temp_dict = {
                        'cod_pl': entry['cod_pl'],
                        'for_period': entry['for_period'],
                        'i_owner': entry['i_owner'],
                        'supplier': entry['supplier'],
                        'cod_u': entry['cod_u'],
                        'servicename': entry['servicename'],
                        'typerec1': 0.0,
                        'typerec2': 0.0,
                        'typerec3': 0.0,
                        'typerec4': 0.0,
                        'typerec5': 0.0,
                        'typerec6': 0.0,
                        'typerec7': 0.0,
                        'typerec8': 0.0,
                        'typerec9': 0.0
                        }
                    temp_dict['typerec' + typerec_str] += s_money_float
                    list_of_dicts.append(temp_dict)
            collection = self.mongodb[str(cod_pl)]
            collection.insert_many(list_of_dicts)
            return True

    def load_collection(self, cod_pl):
        cod_pl = self.check_cod_pl(cod_pl)
        collection = self.mongodb[str(cod_pl)]
        if collection.find_one():
            return collection
        else:
            result = self.load_data_from_sql(cod_pl)
            if result:
                return collection

    def get_suppliers(self, cod_pl):
        collection = self.load_collection(cod_pl)
        if collection:
            pipeline = [
                {'$group': {'_id': {'i_owner': '$i_owner', 'supplier': '$supplier'}}},
                {'$sort': {'_id.i_owner': 1}}
            ]
            return collection.aggregate(pipeline)

    def get_services(self, cod_pl):
        collection = self.load_collection(cod_pl)
        if collection:
            pipeline = [
                {'$group': {'_id': {'cod_u': '$cod_u', 'servicename': '$servicename'}}},
                {'$sort': {'_id.cod_u': 1}}
            ]
            return list(collection.aggregate(pipeline))

    def get_periods(self, cod_pl):
        collection = self.load_collection(cod_pl)
        if collection:
            pipeline = [
                {'$group': {'_id': {'for_period': '$for_period'}}},
                {'$sort': {'_id.for_period': 1}}
            ]
            return list(collection.aggregate(pipeline))

    def get_periods_by_owner(self, cod_pl, i_owner):
        collection = self.load_collection(cod_pl)
        if collection:
            if i_owner:
                return list(collection.find({'i_owner': i_owner}).distinct('for_period'))

    def get_order_data(self, cod_pl, i_owner=None):
        collection = self.load_collection(cod_pl)
        if collection:
            if i_owner:
                return list(collection.find({'i_owner': i_owner}))

