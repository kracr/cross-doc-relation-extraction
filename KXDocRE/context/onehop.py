import json
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from wikidata.client import Client
# Read JSON file
#with open('all_entities.json', 'r') as f:
#    data = json.load(f)

# Extract entities
#entities = data

# Create a file to save the results
#output_file = open('relations.txt', 'w')

# SPARQL endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


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

def get_property_label_with_sparql1(property_id):
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

# Example usage:


def find_property_label(property_id):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={property_id}&format=json&props=labels"
    response = requests.get(url)
    data = response.json()

    # Check if the property ID exists in the response
    if property_id in data["entities"]:
        entity = data["entities"][property_id]
        if "labels" in entity:
            labels = entity["labels"]
            if "en" in labels:
                return labels["en"]["value"]

    # Return None if the property ID or label is not found
    return property_id

def sparql_query(entity_id1,entity_id2):
    # Create a SPARQLWrapper object and set the endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # Define the SPARQL query
    query = f"""
    SELECT ?property WHERE {{
      wd:{entity_id1} ?property wd:{entity_id2}.
    }}
    LIMIT 1
    """

    # Set the query and response format
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the SPARQL query and retrieve the results
    results = sparql.query().convert()

    # Check if there are any results
    if 'results' in results and 'bindings' in results['results']:
        bindings = results['results']['bindings']
        if len(bindings) > 0 and 'property' in bindings[0]:
            property_id = bindings[0]['property']['value'].rsplit('/', 1)[-1]
            return find_property_label(property_id)

    # If no property exists, return None
    return None



def find_onehoprelations(entity1, entity2):
    # Set up the SPARQL endpoint
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setReturnFormat(JSON)

    query1 = """SELECT DISTINCT ?relation1Label ?relation2Label ?zLabel
    WHERE {
    wd:%s ?relation1 ?z.
    ?z ?relation2 wd:%s.
    
    SERVICE wikibase:label { 
        bd:serviceParam wikibase:language "en".
        ?relation1 rdfs:label ?relation1Label.
        ?relation2 rdfs:label ?relation2Label.
        ?z rdfs:label ?zLabel.
    }
    } LIMIT 1
    """ % (entity1, entity2)


    query = """
    SELECT DISTINCT ?relation1 ?relation2 ?z
    WHERE {{
    wd:{entity1_id} ?relation1   ?z.
    ?z  ?relation2 wd:{entity2_id}
    }} LIMIT 1
    """.format(entity1_id=entity1, entity2_id=entity2)

    #print(query)
    sparql.setQuery(query1)

    # Send the SPARQL query and retrieve the results
    results = sparql.query().convert()

    # Extract the relation labels from the query results
    relation_labels1 = [result["relation1Label"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    relation_labels2 = [result["relation2Label"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
    z = [result["zLabel"]["value"].rsplit('/', 1)[-1] for result in results["results"]["bindings"]]
   
    relation_labels1=str(relation_labels1).strip("[]''")
    relation_labels2=str(relation_labels2).strip("[]''")
    z=str(z).strip("[]''")
    #z=mapper.id_to_title(z)


    #relation_labels = relation_labels.rsplit('/', 1)[-1]
    #pred_labels=[result["pred"]["value"] for result in results["results"]["bindings"]]
    #print(i["sub"],i["obj"])

    #try:
    # relation_labels=find_relations(i["sub"],i["obj"])

    # #print("The relations between  are:,",i["sub"],i["obj"],relation_labels)
    #except:
    # pass

    #if(relation_labels1 and relation_labels2 and z):

    # with open("twohop.txt","a+") as g:
    #    g.write(str(entity1)+"\t"+str(r1)+"\t"+str(z)+"\n"+str(z)+"\t"+str(relation_labels2)+"\t"+str(entity2)+"\n")
    return relation_labels1,relation_labels2,z



with open("final_entity_pair.txt","r") as gh:
    for jhoom in gh:
        entity1,entity2=jhoom.split("\t")
        """
        r1,r2,z=find_onehoprelations(entity1,entity2)

        label1 = get_property_label_with_sparql(r1)
        label2 = get_property_label_with_sparql1(r2)
        entitylabel = get_entity_label_with_sparql(z)


        if(r1 and r2 and z):
         with open("full_twohop.txt","a+") as df:
            df.write(entity1.strip())
            df.write("#")
            df.write(entity2.strip())
            df.write("\t")
            df.write(label1.strip())
            df.write("#")
            df.write(label2.strip())
            df.write('#')
            df.write(str(entitylabel).strip())
            df.write("\n")
        """
        relation=sparql_query(entity1, entity2)
        
        if(relation):
         with open("full_onehop.txt","a+") as df:
            df.write(entity1.strip())
            df.write("#")
            entity2=entity2.strip()
            df.write(entity2)
            df.write("\t")
        
            df.write(str(relation).strip())
            df.write("\n")
        
        #print(relation)
        # Construct and execute the SPARQL query

        # Save the results to the file

# Close the output file
#output_file.close()

