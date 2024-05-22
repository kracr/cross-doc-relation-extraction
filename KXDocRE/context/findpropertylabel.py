from wikidata.client import Client

def get_property_label(property_id):
    client = Client()
    entity = client.get('P' + property_id, load=True)
    label = entity.label
    return label

# Example usage:
property_id = '31'  # Change this to the Wikidata property ID you want to look up
label = get_property_label(property_id)
print(f"The label for property {property_id} is: {label}")
