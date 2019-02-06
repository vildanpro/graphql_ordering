def group_periods(periods):
    s_period = 0
    e_period = 0
    ranges = []
    for item in periods:
        period = item.split('-')
        if int(period[1]) + 1 == s_period:
            continue




def get_query(cod_pl):
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
    return query

# ranges_of_periods = graphene.List(RangesOfPeriods,
#                                   i_owner=graphene.Argument(graphene.Int),
#                                   cod_pl=graphene.Argument(graphene.Int))

# def resolve_ranges_of_periods(self, info, i_owner=None, cod_pl=None):
#     if load_data_to_mongo(cod_pl):
#         ranges_of_periods = get_ranges_of_periods(i_owner=i_owner, cod_pl=cod_pl)
#         ranges_of_periods_as_obj_list = []
#         for item in ranges_of_periods:
#             range_of_periods = RangesOfPeriods(item)
#             ranges_of_periods_as_obj_list.append(range_of_periods)
#         return ranges_of_periods_as_obj_list
