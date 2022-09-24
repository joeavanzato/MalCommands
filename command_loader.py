import yaml
import pymongo
import os

def import_to_mongo():
    valid_ckc = ["Reconnaissance", "Weaponization","Delivery","Exploitation","Installation","Command and Control","Actions on Objectives"]
    valid_risk = ["Low","Medium","High","Critical"]
    valid_fidelity = ["Low","Medium","High"]
    valid_os = ["Windows","Linux","Mac"]
    files = []
    for root, dir, f in os.walk("command_data"):
        for i in f:
            p = os.path.join(root, i)
            files.append(p)
    client = pymongo.MongoClient()
    db = client.malcommands_dev
    command_collection = db.command_collection
    technique_collection = db.technique_collection

    for f in files:
        print(f"Loading: {f}")
        with open(f, 'r') as f:
            data = yaml.safe_load(f)
        if data is not None:
            for i in data:
                techs = []
                techniques = []
                tactics = []
                for tactic in i['mitre']:
                    tactics.append(tactic)
                    for technique in i['mitre'][tactic]:
                        techniques.append(technique)
                        tech_req = technique_collection.find_one({'technique_id' : technique})
                        techs.append(tech_req)
                tactics = list(dict.fromkeys(tactics))
                techniques = list(dict.fromkeys(techniques))
                i['mitre_long'] = techs
                i['mitre_tactics'] = tactics
                i['mitre_techniques'] = techniques
                if db.command_collection.count_documents({"command":i['command']}) > 0:
                    filter = {"command":f"{i['command']}"}
                    record = command_collection.update_one(filter, {"$set":i})
                else:
                    command_collection.insert_one(i)


def main():
    import_to_mongo()

main()