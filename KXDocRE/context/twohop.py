
import json
from SPARQLWrapper import SPARQLWrapper, JSON

from SPARQLWrapper import SPARQLWrapper,JSON


import requests

def get_entity_label_with_sparql(entity_id):
    query = f"""
    SELECT ?entityLabel
    WHERE {{
      wd:{entity_id} rdfs:label ?entityLabel.
      FILTER(LANG(?entityLabel) = "en")
    }}
    """
    
    url = 'https://query.wikidata.org/sparql'
    params = {'query': query, 'format': 'json'}
    headers = {'User-Agent': 'YourBotName/0.1 (your@email.com)'}
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        bindings = data['results']['bindings']
        if len(bindings) > 0:
            label = bindings[0]['entityLabel']['value']
            return label
        else:
            return None
    else:
        return None

def get_property_label_with_sparql(property_id):
    query = f"""
    SELECT ?propertyLabel
    WHERE {{
      wd:{property_id} rdfs:label ?propertyLabel.
      FILTER(LANG(?propertyLabel) = "en")
    }}
    """
    
    url = 'https://query.wikidata.org/sparql'
    params = {'query': query, 'format': 'json'}
    headers = {'User-Agent': 'YourBotName/0.1 (your@email.com)'}
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        bindings = data['results']['bindings']
        if len(bindings) > 0:
            label = bindings[0]['propertyLabel']['value']
            return label
        else:
            return None
    else:
        return None



def find_twohoprelations(entity1, entity2):
    # Set up the SPARQL endpoint
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setReturnFormat(JSON)

    query1="""SELECT DISTINCT ?relation1 ?relation2 ?relation3 ?z ?e
    WHERE {{
    wd:{entity1_id} ?relation1 ?z.
    ?z ?relation2 ?e.
    ?e ?relation3 wd:{entity2_id}.
    }}
    LIMIT 1""".format(entity1_id=entity1, entity2_id=entity2)


    query = """
    SELECT DISTINCT ?relation1 ?z ?relation2 ?e ?relation3
    WHERE {{
    wd:{entity1_id} ?relation1   ?z.
    ?z  ?relation2   ?e.
    ?e   ?relation3  wd:{entity2_id}
    }} LIMIT 1
    """.format(entity1_id=entity1, entity2_id=entity2)

    #print(query)
    sparql.setQuery(query)

    # Send the SPARQL query and retrieve the results
    results = sparql.query().convert()

    # Extract the relation labels from the query results
    relation_labels1 = [result["relation1"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    relation_labels2 = [result["relation2"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    z = [result["z"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    e = [result["e"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    relation_labels3 = [result["relation3"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    if relation_labels1 is not None and z is not None and relation_labels2 is not None and e is not None and relation_labels3 is not None:
     relation_labels1=str(relation_labels1).strip("[]''")
     relation_labels2=str(relation_labels2).strip("[]''")
     z=str(z).strip("[]''")
     e=str(e).strip("[]''")
     relation_labels3=str(relation_labels3).strip("[]''")    

     label1 = get_property_label_with_sparql(relation_labels1)
     label2 = get_property_label_with_sparql(relation_labels2)
     label3 = get_property_label_with_sparql(relation_labels3)

     entitylabelz= get_entity_label_with_sparql(z)
     entitylabele= get_entity_label_with_sparql(e)

     #print(relation_labels1,z,relation_labels2,e,relation_labels3)


     #relation_labels = relation_labels.rsplit('/', 1)[-1]
     #pred_labels=[result["pred"]["value"] for result in results["results"]["bindings"]]
     #print(i["sub"],i["obj"])

     #try:
     # relation_labels=find_relations(i["sub"],i["obj"])

     # #print("The relations between  are:,",i["sub"],i["obj"],relation_labels)
     #except:
     # pass
     return label1,entitylabelz,label2,entitylabele,label3
    


"""
# Read JSON file
with open('all_entities.json', 'r') as f:
    data = json.load(f)
entities = data
# Loop through the entities
for i in range(len(entities)):
    for j in range(i+1, len(entities)):
        entity1 = entities[i]
        entity2 = entities[j]

"""
with open("final_entity_pair.txt","r") as gh:
    for jhoom in gh:
        entity1,entity2=jhoom.split("\t")
        entity1=entity1.strip()
        entity2=entity2.strip()
        count=0
        #if(entity1=='Q589953' and entity2=='Q133730'):
        #    count=1
        #if(count==1):
        try:
          relation_labels1,z,relation_labels2,e,relation_labels3=find_twohoprelations(entity1,entity2)
          if(relation_labels1 and z and relation_labels2 and e and relation_labels3):

           with open("full_threehop_latest.txt","a+") as df:
            df.write(entity1.strip())
            df.write("#")
            df.write(entity2.strip())
            df.write("\t")
            df.write(relation_labels1.strip())
            df.write("#")
            df.write(z.strip())
            df.write('#')
            df.write(relation_labels2.strip())
            df.write('#')
            df.write(e.strip())
            df.write('#')
            df.write(relation_labels3.strip())
            df.write("\n")
        except:
           pass

         #relation_labels1,z,relation_labels2,e,relation_labels3=find_twohoprelations(entity1,entity2)
         #if(relation_labels1 and z and relation_labels2 and e and relation_labels3):

#          with open("twohop.txt","a+") as g:
#            g.write(str(entity1)+"\t"+str((relation_labels1))+"\t"+str(z)+"\n"+str(z)+"\t"+str((relation_labels2))+"\t"+str(e)+"\n"+str(e)+"\t"+str((relation_labels3))+"\t"+str(entity2)+"\n")
