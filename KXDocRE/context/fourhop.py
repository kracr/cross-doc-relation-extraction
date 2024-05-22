
import json
from SPARQLWrapper import SPARQLWrapper, JSON

import requests

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


def find_fourhoprelations(entity1, entity2):
    # Set up the SPARQL endpoint
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setReturnFormat(JSON)

    query = """
    SELECT DISTINCT ?relation1 ?z ?relation2 ?e ?relation3 ?f ?relation4 ?g ?relation5
    WHERE {{
    wd:{entity1_id} ?relation1   ?z.
    ?z  ?relation2   ?e.
    ?e   ?relation3   ?f.
    ?f   ?relation4  ?g.
    ?g   ?relation5 wd:{entity2_id}.
    }} LIMIT 1
    """.format(entity1_id=entity1, entity2_id=entity2)

    #print(query)
    sparql.setQuery(query)

    # Send the SPARQL query and retrieve the results
    results = sparql.query().convert()

    # Extract the relation labels from the query results
    relation_labels1 = [result["relation1"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    relation_labels2 = [result["relation2"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    relation_labels3 = [result["relation3"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    relation_labels4 = [result["relation4"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    relation_labels5 = [result["relation5"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]

    z = [result["z"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    e = [result["e"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    f = [result["f"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    g = [result["g"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]


    if relation_labels1 is not None and z is not None and relation_labels2 is not None and e is not None and relation_labels3 is not None and f is not None:
     relation_labels1=str(relation_labels1).strip("[]''")
     relation_labels2=str(relation_labels2).strip("[]''")
     relation_labels3=str(relation_labels3).strip("[]''")
     relation_labels4=str(relation_labels4).strip("[]''")
     relation_labels5=str(relation_labels5).strip("[]''")


     z=str(z).strip("[]''")
     e=str(e).strip("[]''")
     f=str(f).strip("[]''")
     g=str(g).strip("[]''")


     label1 = get_property_label_with_sparql(relation_labels1)
     label2 = get_property_label_with_sparql(relation_labels2)
     label3 = get_property_label_with_sparql(relation_labels3)
     label4 = get_property_label_with_sparql(relation_labels4)

     label5 = get_property_label_with_sparql(relation_labels5)

     entitylabelz= get_entity_label_with_sparql(z)
     entitylabele= get_entity_label_with_sparql(e)
     entitylabelf= get_entity_label_with_sparql(f)
     entitylabelg= get_entity_label_with_sparql(g)




     #print(relation_labels1,z,relation_labels2,e,relation_labels3,f,relation_labels4)

    return label1,entitylabelz, label2,entitylabele, label3,entitylabelf,label4,entitylabelg, label5

   



# Read JSON file
#with open('all_entities.json', 'r') as f:
#    data = json.load(f)
#entities = data
# Loop through the entities
#for i in range(len(entities)):
#    for j in range(i+1, len(entities)):
#        entity1 = entities[i]
#        entity2 = entities[j]

with open("final_entity_pair.txt","r") as gh:
    for jhoom in gh:
        entity1,entity2=jhoom.split("\t")
        entity1=entity1.strip()
        entity2=entity2.strip()
        try:
         relation_labels1,z,relation_labels2,e,relation_labels3,f,relation_labels4,g,relation_labels5=find_fourhoprelations(entity1,entity2)
         if(relation_labels1 and z and relation_labels2 and e and relation_labels3 and f and relation_labels4):

          with open("full_fivehop.txt","a+") as df:
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
            df.write('#')
            df.write(f.strip())
            df.write('#')
            df.write(relation_labels4.strip())
            df.write('#')
            df.write(g.strip())
            df.write('#')
            df.write(relation_labels5.strip())
            df.write("\n")
        except:
         pass



          #with open("threehop.txt","a+") as g:
          #               g.write(entity1+"\t"+str(relation_labels1)+"\t"+str(z)+"\n"+z+"\t"+str(relation_labels2)+"\t"+str(e)+"\n"+str(e)+"\t"+str(relation_labels3)+"\t"+str(f)+"\n"+str(f)+"\t"+str(relation_labels4)+"\t"+str(entity2)+"\n")
          #               #print("The four hop relations between",en1,"and",en2,"is:",relation_labels1,relation_labels2,relation_labels3,relation_labels4)

