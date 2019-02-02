from SPARQLWrapper import SPARQLWrapper
from google.cloud import firestore

from datasource import PricesDataSource

if __name__ == '__main__':

    outcode = 'B1'
    sparql = SPARQLWrapper("http://landregistry.data.gov.uk/landregistry/query")
    db = firestore.Client()

    print("Fetching data for " + outcode)
    datasource = PricesDataSource(outcode)
    datasource.run_query(sparql)

    results = datasource.get_results_dictionary()
    db.collection('outcodes').document(outcode).set(results)