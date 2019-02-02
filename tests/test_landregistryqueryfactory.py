from unittest import TestCase

from datasource.landregistryqueryfactory import LandRegistryQueryFactory
from tests.helpers import strip_whitespace


class LandRegistryQueryFactoryTests(TestCase):
    def test_mainQuery_includesHeaders(self):
        query = strip_whitespace(LandRegistryQueryFactory.main_query('A1'))
        headers = strip_whitespace("""
            PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
            PREFIX  text: <http://jena.apache.org/text#>
            PREFIX  ppd:  <http://landregistry.data.gov.uk/def/ppi/>
            PREFIX  lrcommon: <http://landregistry.data.gov.uk/def/common/>
        """)
        self.assertIn(headers, query)

    def test_mainQuery_includesSelect(self):
        query = strip_whitespace(LandRegistryQueryFactory.main_query('A1'))
        select = strip_whitespace("""SELECT 
            (AVG( ?ppd_pricePaid ) as ?averagePrice) 
            (COUNT( ?item ) as ?transactionCount) 
            (SAMPLE(?ppd_propertyAddressTown) as ?town)
        """)
        self.assertIn(select, query)

    def test_mainQuery_includesWhere(self):
        query = strip_whitespace(LandRegistryQueryFactory.main_query('A1'))
        where = strip_whitespace("""WHERE {
            ?ppd_propertyAddress text:query _:b0 .
            _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> lrcommon:postcode .
            _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b1 .
            _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "( A1 )" .
            _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b2 .
            _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> 3000000 .
            _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .
            ?item ppd:propertyAddress ?ppd_propertyAddress .
            ?item ppd:hasTransaction ?ppd_hasTransaction .
            ?item ppd:pricePaid ?ppd_pricePaid .
            ?item ppd:transactionCategory ?ppd_transactionCategory .
            ?item ppd:transactionDate ?ppd_transactionDate .
            ?item ppd:transactionId ?ppd_transactionId
        """)
        self.assertIn(where, query)

    def test_mainQuery_includesOptional(self):
        query = strip_whitespace(LandRegistryQueryFactory.main_query('A1'))
        optional = strip_whitespace("""
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
        """)
        self.assertIn(optional, query)

    def test_mainQuery_includesYearRangeFilter(self):
        query = strip_whitespace(LandRegistryQueryFactory.main_query('A1'))
        year_range_filter_from = strip_whitespace("FILTER ( ?ppd_transactionDate >= ")
        year_range_filter_to = strip_whitespace("FILTER ( ?ppd_transactionDate <= ")
        self.assertIn(year_range_filter_from, query)
        self.assertIn(year_range_filter_to, query)

    def test_typeQuery_includesHeaders(self):
        query = strip_whitespace(LandRegistryQueryFactory.type_query('A1'))
        headers = strip_whitespace("""
            PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
            PREFIX  text: <http://jena.apache.org/text#>
            PREFIX  ppd:  <http://landregistry.data.gov.uk/def/ppi/>
            PREFIX  lrcommon: <http://landregistry.data.gov.uk/def/common/>
        """)
        self.assertIn(headers, query)

    def test_typeQuery_includesSelect(self):
        query = strip_whitespace(LandRegistryQueryFactory.type_query('A1'))
        select = strip_whitespace("""SELECT 
            (AVG( ?ppd_pricePaid ) as ?averagePrice) 
            (COUNT( ?item ) as ?transactionCount) 
            ?ppd_propertyType
        """)
        self.assertIn(select, query)

    def test_typeQuery_includesWhere(self):
        query = strip_whitespace(LandRegistryQueryFactory.type_query('A1'))
        where = strip_whitespace("""WHERE {
            ?ppd_propertyAddress text:query _:b0 .
            _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> lrcommon:postcode .
            _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b1 .
            _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "( A1 )" .
            _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b2 .
            _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> 3000000 .
            _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .
            ?item ppd:propertyAddress ?ppd_propertyAddress .
            ?item ppd:hasTransaction ?ppd_hasTransaction .
            ?item ppd:pricePaid ?ppd_pricePaid .
            ?item ppd:transactionCategory ?ppd_transactionCategory .
            ?item ppd:transactionDate ?ppd_transactionDate .
            ?item ppd:transactionId ?ppd_transactionId . 
            ?item ppd:propertyType ?ppd_propertyType
        """)
        self.assertIn(where, query)

    def test_typeQuery_includesOptional(self):
        query = strip_whitespace(LandRegistryQueryFactory.type_query('A1'))
        optional = strip_whitespace("""
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
        """)
        self.assertIn(optional, query)

    def test_typeQuery_includesGroupBy(self):
        query = strip_whitespace(LandRegistryQueryFactory.type_query('A1'))
        group_by = strip_whitespace("GROUP BY ?ppd_propertyType")
        self.assertIn(group_by, query)

    def test_typeQuery_includesYearRangeFilter(self):
        query = strip_whitespace(LandRegistryQueryFactory.type_query('A1'))
        year_range_filter_from = strip_whitespace("FILTER ( ?ppd_transactionDate >= ")
        year_range_filter_to = strip_whitespace("FILTER ( ?ppd_transactionDate <= ")
        self.assertIn(year_range_filter_from, query)
        self.assertIn(year_range_filter_to, query)
