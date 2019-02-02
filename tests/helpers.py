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
