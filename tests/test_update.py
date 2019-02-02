from unittest import TestCase

from mockfirestore import MockFirestore

from tests.helpers import MockSparqlWrapper
from update import update_price_data, outcodes


class UpdateTests(TestCase):

    def setUp(self):
        self.mock_db = MockFirestore()

    def test_updatesHousePriceData(self):
        mock_sparql = MockSparqlWrapper()
        mock_sparql.stub_responses('ABERDEEN', avg_price=500000, transaction_count=500)

        update_price_data(self.mock_db, mock_sparql)

        self.assertEqual('json', mock_sparql.return_format)
        self.assertOutcodeInQuery('AB10', mock_sparql.queries[1])
        self.assertQuerySelectsOverall(mock_sparql.queries[1])

        results = self.mock_db.collection('outcodes').document('AB10').get().to_dict()

        self.assertEqual('Aberdeen', results['areaName'])
        self.assertEqual(500000, results['averagePrice'])
        self.assertEqual('AB10', results['outcode'])
        self.assertEqual(500, results['transactionCount'])

    def test_updatesTypePriceData(self):
        mock_sparql = MockSparqlWrapper()
        mock_sparql.stub_responses(
            'ABERDEEN',
            avg_price=500000,
            transaction_count=500,
            terraced=100000,
            detached=200000,
            semi=300000,
            flat=400000
        )

        update_price_data(self.mock_db, mock_sparql)

        self.assertEqual('json', mock_sparql.return_format)
        self.assertOutcodeInQuery('AB10', mock_sparql.queries[1])
        self.assertQuerySelectsByType(mock_sparql.queries[1])

        results = self.mock_db.collection('outcodes').document('AB10').get().to_dict()

        self.assertEqual(100000, results['terracedAverage'])
        self.assertEqual(200000, results['detachedAverage'])
        self.assertEqual(300000, results['semiDetachedAverage'])
        self.assertEqual(400000, results['flatAverage'])

    def test_updatesAllOutcodes(self):
        mock_sparql = MockSparqlWrapper()
        mock_sparql.stub_responses()

        update_price_data(self.mock_db, mock_sparql)

        self.assertEqual(len(outcodes) * 2, mock_sparql.request_count)
        self.assertEqual(len(outcodes), len(self.mock_db.collection('outcodes').get()))

    def assertOutcodeInQuery(self, outcode, query):
        self.assertIn(f'_:b1<http://www.w3.org/1999/02/22-rdf-syntax-ns#first>"({outcode})".', query)

    def assertQuerySelectsOverall(self, query):
        self.assertIn(
            'SELECT(AVG(?ppd_pricePaid)as?averagePrice)(COUNT(?item)as?transactionCount)',
            query
        )

    def assertQuerySelectsByType(self, query):
        self.assertIn(
            'SELECT(AVG(?ppd_pricePaid)as?averagePrice)(COUNT(?item)as?transactionCount)?ppd_propertyType',
            query
        )
