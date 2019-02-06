from mssql import BaseDBQuery
from pymongo import MongoClient

client = MongoClient('mongodb', 27017)
# client.drop_database('order_data')
mongodb = client.order_data


class MSqlDBLoader(BaseDBQuery):
    def query_data(self, cod_pl):
        if not isinstance(cod_pl, int):
            return {'Error': 'COD_PL is not INT'}
        else:
            collection = mongodb[str(cod_pl)]
            if collection.find_one():
                return True
            else:
                query = f"""
SELECT 
    t.[COD_PL], t.[COD_U], [for_period] = asup.dbo.fnmonthtodate(t.[for_period]), t.[TypeRec], t.[s_money], o.I_Owner, 
    serviceName=isnull(sg_2.GroupName, sg_1.GroupName), o.NAME AS Supplier
FROM 
    buh.dbo.sum_table t
INNER JOIN 
    asup.dbo.flats_system fs ON fs.i_lschet=t.COD_PL
INNER JOIN 
    asup.dbo.objservices s ON s.id = t.cod_u
LEFT JOIN 
    buh.dbo.service_group_house sgh WITH (NOLOCK) ON sgh.i_house = fs.i_house AND sgh.cod_u = s.id
LEFT JOIN 
    buh.dbo.SERVICE_Group sg_1 WITH (NOLOCK) ON sg_1.GroupID =isnull(sgh.groupid, s.GroupID) AND sg_1.I_CITY = 0
LEFT JOIN 
    buh.dbo.SERVICE_Group sg_2 WITH (NOLOCK) ON sg_2.GroupID = isnull(sgh.groupid,s.GroupID) 
AND sg_2.I_CITY = fs.i_city
LEFT JOIN 
    buh.dbo.OwnerProperties op WITH (NOLOCK) ON 1 = 1 AND op.OwnerID = t.I_OWNER
LEFT JOIN 
    buh.dbo.OWNER o WITH (NOLOCK) ON 1 = 1 AND o.I_OWNER = op.ReportOwner
WHERE 
    COD_PL = {cod_pl} AND o.NAME IS NOT NULL AND TypeRec >0
                        """
                cursor = self.call(query)
                if cursor.rowcount == 0:
                    cursor.close()
                    result = None
                else:
                    result = cursor.fetchall()
                    cursor.close()
                if not result:
                    return {'Error': 'Not found'}
                else:
                    list_of_dicts = list()
                    for r in result:
                        entry = self.to_dict(r)
                        entry['s_money'] = float(entry['s_money'])
                        index = None
                        if len(list_of_dicts) > 0:
                            for i, item in enumerate(list_of_dicts):
                                if (
                                        item['for_period'] == entry['for_period'] and
                                        item['i_owner'] == entry['i_owner'] and
                                        item['cod_u'] == entry['cod_u']
                                ):
                                    index = i
                                    break
                        if index:
                            list_of_dicts[index]['s_money'].append({
                                'typerec': entry['typerec'], 's_money': float(entry['s_money'])})
                        else:
                            list_of_dicts.append(
                                {
                                    'cod_pl': entry['cod_pl'],
                                    'for_period': entry['for_period'],
                                    'i_owner': entry['i_owner'],
                                    'supplier': entry['supplier'],
                                    'cod_u': entry['cod_u'],
                                    'servicename': entry['servicename'],
                                    's_money': [{'typerec': entry['typerec'], 's_money': float(entry['s_money'])}]
                                }
                            )
                    collection = mongodb[str(cod_pl)]
                    collection.insert_many(list_of_dicts)
                    return True


def get_supplers(cod_pl):
    collection = mongodb[str(cod_pl)]
    pipeline = [
        {'$group': {'_id': {'i_owner': '$i_owner', 'supplier': '$supplier'}}},
        {'$sort': {'_id.i_owner': 1}}
    ]
    return list(collection.aggregate(pipeline))


def get_services(cod_pl):
    collection = mongodb[str(cod_pl)]
    pipeline = [
        {'$group': {'_id': {'cod_u': '$cod_u', 'servicename': '$servicename'}}},
        {'$sort': {'_id.cod_u': 1}}
    ]
    return list(collection.aggregate(pipeline))


def get_periods(cod_pl):
    collection = mongodb[str(cod_pl)]
    pipeline = [
        {'$group': {'_id': {'for_period': '$for_period'}}},
        {'$sort': {'_id.for_period': 1}}
    ]
    return list(collection.aggregate(pipeline))


def get_periods_by_owner(cod_pl, i_owner):
    collection = mongodb[str(cod_pl)]
    return collection.find({'i_owner': i_owner}).distinct('for_period')


def get_order_data(cod_pl, i_owner=None):
    collection = mongodb[str(cod_pl)]
    if i_owner:
        return collection.find({'i_owner': i_owner})
