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



