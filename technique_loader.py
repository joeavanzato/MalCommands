from pyattck import Attck
import yaml
import pymongo



def build_yaml():
    # Iterate through PyAttck Technique details and extract relevant information for a YAML dump - could just insert directly here as well
    attack = Attck(nested_techniques=False)
    t_list = []
    t_ids = []
    for technique in attack.enterprise.techniques:
        tech = {}
        description = technique.description
        object_id = technique.technique_id
        name = technique.name
        #print(object_id)
        tech['name'] = name
        tech['technique_id'] = object_id
        if object_id in t_ids:
            continue
        else:
            t_ids.append(object_id)
        tech['description'] = description
        for ref in technique.external_references:
            if ref.source_name == "mitre-attack":
                technique_url = ref.url
                break
        tech['url'] = technique_url
        tech['tactics'] = []
        for tactic in technique.tactics:
            tech['tactics'].append(tactic.name)
        t_list.append(tech)
    with open('technique_reference.yml', 'w') as f:
        yaml.dump(t_list, f)

def import_to_mongo():
    client = pymongo.MongoClient()
    db = client.malcommands_dev
    technique_collection = db.technique_collection
    with open('technique_reference.yml', 'r') as f:
        data = yaml.safe_load(f)
    for i in data:
        # If the technique already exists, just update with any modifications, otherwise insert it.
        if db.technique_collection.count_documents({"technique_id":i['technique_id']}) > 0:
            filter = {"technique_id":f"{i['technique_id']}"}
            record = technique_collection.update_one(filter, {"$set":i})
        else:
            technique_collection.insert_one(i)


def main():
    #build_yaml()
    import_to_mongo()

main()