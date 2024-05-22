from wikidataintegrator import wdi_core

# Replace 'Q42' with your desired Wikidata ID
wikidata_id = 'Q42'

query = """
SELECT ?item ?itemLabel
WHERE
{
  ?item skos:altLabel ?itemLabel .
  FILTER(STR(?item) = "http://www.wikidata.org/entity/"""+wikidata_id+"""") .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""

synonyms = wdi_core.WDItemEngine.execute_sparql_query(query)

if synonyms['results']['bindings']:
    print("Synonyms of the Wikidata ID {}:".format(wikidata_id))
    for result in synonyms['results']['bindings']:
        print(result['itemLabel']['value'])
else:
    print("No synonyms found for the Wikidata ID {}.".format(wikidata_id))

