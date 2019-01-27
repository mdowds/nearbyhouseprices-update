from datetime import datetime
from dateutil.relativedelta import relativedelta


# TODO add unit tests
class LandRegistryQuery:

    headers = """
        PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
        PREFIX  text: <http://jena.apache.org/text#>
        PREFIX  ppd:  <http://landregistry.data.gov.uk/def/ppi/>
        PREFIX  lrcommon: <http://landregistry.data.gov.uk/def/common/>
    """

    select = "SELECT"

    where = """
            ?ppd_propertyAddress text:query _:b0 .
            _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> lrcommon:postcode .
            _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b1 .
            _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "( {} )" .
            _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b2 .
            _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> 3000000 .
            _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .
            ?item ppd:propertyAddress ?ppd_propertyAddress .
            ?item ppd:hasTransaction ?ppd_hasTransaction .
            ?item ppd:pricePaid ?ppd_pricePaid .
            ?item ppd:transactionCategory ?ppd_transactionCategory .
            ?item ppd:transactionDate ?ppd_transactionDate .
            ?item ppd:transactionId ?ppd_transactionId
        """

    optional = """
            OPTIONAL
              { ?item ppd:estateType ?ppd_estateType }
            OPTIONAL
              { ?item ppd:newBuild ?ppd_newBuild }
            OPTIONAL
              { ?ppd_propertyAddress lrcommon:county ?ppd_propertyAddressCounty }
            OPTIONAL
              { ?ppd_propertyAddress lrcommon:district ?ppd_propertyAddressDistrict }
            OPTIONAL
              { ?ppd_propertyAddress lrcommon:locality ?ppd_propertyAddressLocality }
            OPTIONAL
              { ?ppd_propertyAddress lrcommon:paon ?ppd_propertyAddressPaon }
            OPTIONAL
              { ?ppd_propertyAddress lrcommon:postcode ?ppd_propertyAddressPostcode }
            OPTIONAL
              { ?ppd_propertyAddress lrcommon:saon ?ppd_propertyAddressSaon }
            OPTIONAL
              { ?ppd_propertyAddress lrcommon:street ?ppd_propertyAddressStreet }
            OPTIONAL
              { ?ppd_propertyAddress lrcommon:town ?ppd_propertyAddressTown }
            OPTIONAL
              { ?item ppd:propertyType ?ppd_propertyType }
            OPTIONAL
              { ?item ppd:recordStatus ?ppd_recordStatus }
        """

    filter = ""

    groupby = ""

    def __init__(self, outcode):
        self.where = self.where.format(outcode)

    def get_querystring(self):
        return self.headers + self.select + " WHERE {" + self.where + self.optional + self.filter + "}" + self.groupby

    def add_averageprice(self):
        self.select += " (AVG( ?ppd_pricePaid ) as ?averagePrice)"

    def add_transactioncount(self):
        self.select += " (COUNT( ?item ) as ?transactionCount)"

    def add_town(self):
        self.select += " (SAMPLE(?ppd_propertyAddressTown) as ?town)"

    def add_propertytype_select(self):
        self.select += " ?ppd_propertyType"

    def add_propertytype_where(self):
        self.where += " . ?item ppd:propertyType ?ppd_propertyType"

    def add_year_range(self, fromRange, toRange):
        self.filter += "FILTER ( ?ppd_transactionDate >= \"{}\"^^xsd:date".format(
            self.calculate_querydate(fromRange)) + " )"
        self.filter += "FILTER ( ?ppd_transactionDate <= \"{}\"^^xsd:date".format(
            self.calculate_querydate(toRange)) + " )"

    def add_groupby(self, group):
        if group == 'type':
            self.groupby = " GROUP BY ?ppd_propertyType"

    def calculate_querydate(self, yearRange):
        beginningDate = datetime.now() - relativedelta(years=yearRange, months=2)
        return beginningDate.strftime("%Y-%m-%d")