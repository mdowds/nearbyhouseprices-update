from SPARQLWrapper import SPARQLWrapper

from .landregistryinterface import LandRegistryInterface, LandRegistryInterfaceError
from .landregistryqueryfactory import LandRegistryQueryFactory


class PricesDataSource:

    # Constants
    CURRENT_YEAR_MAX = 1
    CURRENT_YEAR_MIN = 0

    TYPE_KEY = 'type'
    PROPERTYTYPE_KEY = 'ppd_propertyType'
    ERROR_KEY = 'error'
    RESULTS_KEY = 'results'
    BINDINGS_KEY = 'bindings'
    TOWN_KEY = 'town'
    VALUE_KEY = 'value'

    OUTCODE_KEY = 'outcode'
    AREANAME_KEY = 'areaName'
    AVERAGEPRICE_KEY = 'averagePrice'
    TRANSACTIONCOUNT_KEY = 'transactionCount'
    DETACHEDAVERAGE_KEY = 'detachedAverage'
    SEMIAVERAGE_KEY = 'semiDetachedAverage'
    TERRACEDAVERAGE_KEY = 'terracedAverage'
    FLATAVERAGE_KEY = 'flatAverage'

    def __init__(self, outcode):
        self.outcode = outcode.upper()
        self.error = None
        self.output = {}

    def run_query(self, sparql: SPARQLWrapper):
        # Main query
        main_query = LandRegistryQueryFactory.main_query(self.outcode)
        try:
            self.main_query_results = LandRegistryInterface.run_query(sparql, main_query)
        except LandRegistryInterfaceError as error:
            self.error = str(error)
            return

        # Property type query
        type_query = LandRegistryQueryFactory.type_query(self.outcode)
        self.type_query_results = LandRegistryInterface.run_query(sparql, type_query)

        self.process_results()

    # Return results

    def get_results_dictionary(self):
        self.output[self.OUTCODE_KEY] = self.outcode

        if self.error is not None:
            raise PricesDataSourceError(self.error)

        return self.output

    # Helper methods

    def process_results(self):

        if self.check_errors(self.main_query_results):
            return

        results = self.main_query_results[self.RESULTS_KEY][self.BINDINGS_KEY][0]
        type_results = self.type_query_results[self.RESULTS_KEY][self.BINDINGS_KEY]

        self.output[self.AREANAME_KEY] = results[self.TOWN_KEY][self.VALUE_KEY].title()
        self.output[self.AVERAGEPRICE_KEY] = int(float(results[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))
        self.output[self.TRANSACTIONCOUNT_KEY] = int(results[self.TRANSACTIONCOUNT_KEY][self.VALUE_KEY])

        for binding in type_results:

            if self.check_type(binding, "detached"):
                self.output[self.DETACHEDAVERAGE_KEY] = int(float(binding[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))
            elif self.check_type(binding, "semi-detached"):
                self.output[self.SEMIAVERAGE_KEY] = int(float(binding[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))
            elif self.check_type(binding, "terraced"):
                self.output[self.TERRACEDAVERAGE_KEY] = int(float(binding[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))
            elif self.check_type(binding, "flat-maisonette"):
                self.output[self.FLATAVERAGE_KEY] = int(float(binding[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))

    def check_type(self, binding, propertyType):
        type_def_url = "http://landregistry.data.gov.uk/def/common/"

        if (self.PROPERTYTYPE_KEY in binding and
                binding[self.PROPERTYTYPE_KEY][self.VALUE_KEY] == type_def_url + propertyType
                and int(binding[self.TRANSACTIONCOUNT_KEY][self.VALUE_KEY]) > 0):
            return True
        else:
            return False

    def check_errors(self, results):
        if type(results) == str and results[:5] == "Error":
            self.error = "Error in query"
            return True

        if len(results[self.RESULTS_KEY][self.BINDINGS_KEY]) == 0:
            self.error = "No results found"
            return True

        transaction_count = int(results[self.RESULTS_KEY][self.BINDINGS_KEY][0][self.TRANSACTIONCOUNT_KEY][self.VALUE_KEY])

        if transaction_count == 0:
            self.error = "No transactions for outcode"
            return True

        return False


class PricesDataSourceError(Exception):
    pass
