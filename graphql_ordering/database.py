from pprint import pprint

import mongoengine
from .mssqldb import MSqlDBLoader as Loader
from .models import Money, money_schema
from .cluster import cluster


def create_monog_db(mongo_db=None):
    if isinstance(mongo_db, type(mongoengine)):
        mongo_db = mongo_db
    else:
        mongo_db = mongoengine
    if getattr(mongo_db, '__created__', None):
        return mongo_db
    mongo_db.connect(db='test', host='mongodb', port=27017)
    mongo_db.__created__ = True
    return mongo_db


def load_data_to_mongo(cod_pl):
    if not Money.objects(cod_pl=cod_pl).first():
        data_sql = Loader().query_to_mssql(cod_pl)
        for item in data_sql:
            d, errors = money_schema.load(item)
            d.save()


    return True


def get_suppliers(cod_pl):
    if load_data_to_mongo(cod_pl):
        pipeline = [
            {'$group': {'_id': {'i_owner': '$i_owner', 'supplier': '$supplier', 'cod_pl': '$cod_pl'}}},
            {'$sort': {'_id.i_owner': 1}}
        ]
        cursor = Money.objects.aggregate(*pipeline)
        suppliers = [item['_id'] for item in cursor]
        return suppliers


def get_ranges_of_periods(cod_pl, i_owner):
    if load_data_to_mongo(cod_pl):
        ranges_of_periods = list()
        if i_owner:
            pipeline = [
                {'$match': {'cod_pl': cod_pl, 'i_owner': i_owner}},
                {'$group': {'_id': {'i_owner': '$i_owner', 'for_period': '$for_period'}}}
            ]
            cursor = Money.objects.aggregate(*pipeline)
            data = [item['_id']['for_period'] for item in cursor]
            data_group = cluster(data, maxgap=2)
            ranges_of_periods = []
            for item in data_group:
                first = item[0]
                last = item[-1]
                period = str(first) + '-' + str(last)
                ranges_of_periods.append(period)

        return ranges_of_periods


def get_owner_periods(cod_pl, i_owner):
    if load_data_to_mongo(cod_pl):
        owner_periods = list()
        if i_owner:
            owner_periods = Money.objects(cod_pl=cod_pl, i_owner=i_owner).distinct('for_period')
        return sorted(owner_periods)


def get_order_data(cod_pl, i_owner, range_of_periods):
    range_of_periods = range_of_periods.split('-')
    start_period = int(range_of_periods[0])
    end_period = int(range_of_periods[1])

    pipeline = [
        {
            '$match':
                {
                    'cod_pl': cod_pl,
                    'i_owner': i_owner,
                    'for_period':
                        {
                            '$gt': start_period, '$lte': end_period
                        }
                }
        },

        {
            '$addFields':
                {
                    'typerec_1':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', 1]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_2':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', 2]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_minus60':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', -60]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_6':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', 6]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_7':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', 7]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_9':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', 9]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_minus66':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', -66]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_minus10':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', -10]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_minus7':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', -7]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_minus6':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', -6]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        },
                    'typerec_minus1':
                        {
                            '$cond':
                                {
                                    'if': {'$eq': ['$typerec', -1]},
                                    'then': '$s_money',
                                    'else': 0
                                }
                        }
                }
        },

        {
            '$project':
                {
                    '_id': 0, 's_money': 0, 'typerec': 0
                },
        },

        {
            '$group':
                {
                    '_id':
                        {
                            'cod_pl': '$cod_pl', 'i_owner': '$i_owner', 'supplier': '$supplier',
                            'for_period': '$for_period', 'cod_u': '$cod_u', 'servicename': '$servicename',
                        },
                    'typerec_1': {'$sum': '$typerec_1'},
                    'typerec_2': {'$sum': '$typerec_2'},
                    'typerec_minus60': {'$sum': '$typerec_minus60'},
                    'typerec_6': {'$sum': '$typerec_6'},
                    'typerec_7': {'$sum': '$typerec_7'},
                    'typerec_9': {'$sum': '$typerec_9'},
                    'typerec_minus66': {'$sum': '$typerec_minus66'},
                    'typerec_minus10': {'$sum': '$typerec_minus10'},
                    'typerec_minus7': {'$sum': '$typerec_minus7'},
                    'typerec_minus6': {'$sum': '$typerec_minus6'},
                    'typerec_minus1': {'$sum': '$typerec_minus1'}
                }
        },

        {
            '$addFields':
                {
                    'total':
                        {
                            '$sum':
                                [
                                    '$typerec_1', '$typerec_2', '$typerec_minus60', '$typerec_6',
                                    '$typerec_7', '$typerec_9', '$typerec_minus66', '$typerec_minus10',
                                    '$typerec_minus7', '$typerec_minus6', '$typerec_minus1'
                                ]
                        }
                }
        },
        {
            '$sort': {'_id.for_period': 1}
        }
    ]
    cursor = Money.objects.aggregate(*pipeline)
    return list(cursor)


