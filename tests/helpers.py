def strip_whitespace(string: str) -> str:
    return ''.join(string.split())


class MockSparqlWrapper:

    def __init__(self):
        self.return_format = ''
        self.queries = []
        self.results_to_return = [{}, {}]
        self.request_count = 0

    # Mocked methods

    def setReturnFormat(self, return_format):
        self.return_format = return_format

    def setQuery(self, query):
        self.queries.append(strip_whitespace(query))

    def queryAndConvert(self):
        self.request_count += 1
        call_count_is_even = self.request_count % 2 == 0
        result_to_return = self.results_to_return[1] if call_count_is_even else self.results_to_return[0]
        return result_to_return

    # Test helpers

    def stub_responses(self, place_name='', avg_price=0, transaction_count=1, terraced=0, detached=0, flat=0, semi=0):
        main_response = {
            'head': {'vars': ['averagePrice', 'transactionCount', 'town']},
            'results': {
                'bindings': [{
                    'averagePrice': {
                        'type': 'literal',
                        'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
                        'value': avg_price
                    },
                    'transactionCount': {
                        'type': 'literal',
                        'datatype': 'http://www.w3.org/2001/XMLSchema#integer',
                        'value': transaction_count
                    },
                    'town': {'type': 'literal', 'value': place_name}
                }]
            }
        }

        type_response = {
            'head': {'vars': ['averagePrice', 'transactionCount', 'ppd_propertyType']},
            'results': {
                'bindings': [
                    {
                        'averagePrice': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
                            'value': terraced
                        },
                        'transactionCount': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#integer',
                            'value': '100'
                        },
                        'ppd_propertyType': {
                            'type': 'uri',
                            'value': 'http://landregistry.data.gov.uk/def/common/terraced'
                        }
                    },
                    {
                        'averagePrice': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
                            'value': detached
                        },
                        'transactionCount': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#integer',
                            'value': '100'
                        },
                        'ppd_propertyType': {
                            'type': 'uri',

                            'value': 'http://landregistry.data.gov.uk/def/common/detached'
                        }
                    },
                    {
                        'averagePrice': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
                            'value': semi
                        },
                        'transactionCount': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#integer',
                            'value': '100'
                        },
                        'ppd_propertyType': {
                            'type': 'uri',
                            'value': 'http://landregistry.data.gov.uk/def/common/semi-detached'
                        }
                    },
                    {
                        'averagePrice': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
                            'value': flat
                        },
                        'transactionCount': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#integer',
                            'value': '100'
                        },
                        'ppd_propertyType': {
                            'type': 'uri',
                            'value': 'http://landregistry.data.gov.uk/def/common/flat-maisonette'
                        }
                    },
                    {
                        'averagePrice': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
                            'value': '0'
                        },
                        'transactionCount': {
                            'type': 'literal',
                            'datatype': 'http://www.w3.org/2001/XMLSchema#integer',
                            'value': '0'
                        },
                        'ppd_propertyType': {
                            'type': 'uri',
                            'value': 'http://landregistry.data.gov.uk/def/common/otherPropertyType'
                        }
                    }
                ]}
        }

        self.results_to_return = [main_response, type_response]

    def expected_price_query(self, outcode):
        expected = """
            PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
            PREFIX  text: <http://jena.apache.org/text#>
            PREFIX  ppd:  <http://landregistry.data.gov.uk/def/ppi/>
            PREFIX  lrcommon: <http://landregistry.data.gov.uk/def/common/>
            SELECT (AVG( ?ppd_pricePaid ) as ?averagePrice) (COUNT( ?item ) as ?transactionCount) 
            (SAMPLE(?ppd_propertyAddressTown) as ?town) 
            WHERE {
                ?ppd_propertyAddress text:query _:b0 .
                _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> lrcommon:postcode .
                _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b1 .
                _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "( %s )" .
                _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b2 .
                _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> 3000000 .
                _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .
                ?item ppd:propertyAddress ?ppd_propertyAddress .
                ?item ppd:hasTransaction ?ppd_hasTransaction .
                ?item ppd:pricePaid ?ppd_pricePaid .
                ?item ppd:transactionCategory ?ppd_transactionCategory .
                ?item ppd:transactionDate ?ppd_transactionDate .
                ?item ppd:transactionId ?ppd_transactionId
            
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
                FILTER ( ?ppd_transactionDate >= "2017-11-27"^^xsd:date )
                FILTER ( ?ppd_transactionDate <= "2018-11-27"^^xsd:date )
            }
        """ % outcode
        return strip_whitespace(expected)

    def expected_types_query(self, outcode):
        expected = """
            PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
            PREFIX  text: <http://jena.apache.org/text#>
            PREFIX  ppd:  <http://landregistry.data.gov.uk/def/ppi/>
            PREFIX  lrcommon: <http://landregistry.data.gov.uk/def/common/>
            SELECT (AVG( ?ppd_pricePaid ) as ?averagePrice) (COUNT( ?item ) as ?transactionCount) ?ppd_propertyType
            WHERE {
                ?ppd_propertyAddress text:query _:b0 .
                _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> lrcommon:postcode .
                _:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b1 .
                _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "( %s )" .
                _:b1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:b2 .
                _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> 3000000 .
                _:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .
                ?item ppd:propertyAddress ?ppd_propertyAddress .
                ?item ppd:hasTransaction ?ppd_hasTransaction .
                ?item ppd:pricePaid ?ppd_pricePaid .
                ?item ppd:transactionCategory ?ppd_transactionCategory .
                ?item ppd:transactionDate ?ppd_transactionDate .
                ?item ppd:transactionId ?ppd_transactionId
                . ?item ppd:propertyType ?ppd_propertyType
                OPTIONAL { ?item ppd:estateType ?ppd_estateType }
                OPTIONAL { ?item ppd:newBuild ?ppd_newBuild }
                OPTIONAL { ?ppd_propertyAddress lrcommon:county ?ppd_propertyAddressCounty }
                OPTIONAL { ?ppd_propertyAddress lrcommon:district ?ppd_propertyAddressDistrict }
                OPTIONAL { ?ppd_propertyAddress lrcommon:locality ?ppd_propertyAddressLocality }
                OPTIONAL { ?ppd_propertyAddress lrcommon:paon ?ppd_propertyAddressPaon }
                OPTIONAL { ?ppd_propertyAddress lrcommon:postcode ?ppd_propertyAddressPostcode }
                OPTIONAL { ?ppd_propertyAddress lrcommon:saon ?ppd_propertyAddressSaon }
                OPTIONAL { ?ppd_propertyAddress lrcommon:street ?ppd_propertyAddressStreet }
                OPTIONAL { ?ppd_propertyAddress lrcommon:town ?ppd_propertyAddressTown }
                OPTIONAL { ?item ppd:propertyType ?ppd_propertyType }
                OPTIONAL { ?item ppd:recordStatus ?ppd_recordStatus }
                FILTER ( ?ppd_transactionDate >= "2017-11-27"^^xsd:date )
                FILTER ( ?ppd_transactionDate <= "2018-11-27"^^xsd:date )
            }
            GROUP BY ?ppd_propertyType
        """ % outcode
        return strip_whitespace(expected)
