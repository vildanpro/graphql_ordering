from mssql import BaseDBQuery


class MSqlDBLoader(BaseDBQuery):

    def query_to_mssql(self, cod_pl):
        query = f"""
SELECT t.[COD_PL]
     ,t.[COD_U]
     ,t.[ID]
     ,t.[for_period]
     ,t.[TypeRec]
     ,t.[s_money]
     ,o.I_Owner,
   serviceName=isnull(sg_2.GroupName, sg_1.GroupName),
   o.NAME AS Supplier
 FROM
   buh.dbo.sum_table t  --t1
INNER JOIN
   asup.dbo.flats_system fs on fs.i_lschet=t.COD_PL
INNER JOIN
   asup.dbo.objservices s on  --t2
   s.id = t.cod_u
LEFT JOIN
   buh.dbo.service_group_house sgh WITH (NOLOCK) ON  --t3
   sgh.i_house = fs.i_house AND sgh.cod_u = s.id
LEFT JOIN
   buh.dbo.SERVICE_Group sg_1 WITH (NOLOCK) ON
   sg_1.GroupID =isnull(sgh.groupid, s.GroupID) AND sg_1.I_CITY = 0
LEFT JOIN
   buh.dbo.SERVICE_Group sg_2 WITH (NOLOCK) ON
   sg_2.GroupID = isnull(sgh.groupid,s.GroupID) AND sg_2.I_CITY = fs.i_city
LEFT JOIN
   buh.dbo.OwnerProperties op WITH (NOLOCK) ON
   1 = 1 AND op.OwnerID = t.I_OWNER            -- ReportOwner
LEFT JOIN
   buh.dbo.OWNER o WITH (NOLOCK) ON
   1 = 1 AND o.I_OWNER = op.ReportOwner
WHERE
   COD_PL = {cod_pl} AND o.NAME IS NOT NULL
"""

        cursor = self.call(query)
        if cursor.rowcount == 0:
            cursor.close()
            result = None
        else:
            result = cursor.fetchall()

        return [self.to_dict(r) for r in result] if result is not None else list()
