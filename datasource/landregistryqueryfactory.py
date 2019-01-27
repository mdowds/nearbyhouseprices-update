from .landregistryquery import LandRegistryQuery


class LandRegistryQueryFactory:

    # Constants
    CURRENT_YEAR_MAX = 1
    CURRENT_YEAR_MIN = 0
    PAST_YEAR_MAX = 2
    PAST_YEAR_MIN = 1

    TYPE_KEY = 'type'

    @classmethod
    def main_query(cls, outcode):
        query = cls.base_query(outcode)
        query.add_town()
        query.add_year_range(cls.CURRENT_YEAR_MAX, cls.CURRENT_YEAR_MIN)

        return query.get_querystring()

    @classmethod
    def type_query(cls, outcode):
        query = cls.base_query(outcode)
        query.add_year_range(cls.CURRENT_YEAR_MAX, cls.CURRENT_YEAR_MIN)
        query.add_propertytype_select()
        query.add_propertytype_where()
        query.add_groupby(cls.TYPE_KEY)

        return query.get_querystring()

    # Helper methods

    @classmethod
    def base_query(cls, outcode):
        query = LandRegistryQuery(outcode)
        query.add_averageprice()
        query.add_transactioncount()

        return query