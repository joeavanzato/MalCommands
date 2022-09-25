import yaml
import pymongo
import os

def import_to_mongo():
    valid_ckc = ["Reconnaissance", "Weaponization","Delivery","Exploitation","Installation","Command and Control","Actions on Objectives"]
    valid_tactics = ["Reconnaissance","Resource Development","Initial Access","ML Model Access","Execution","Persistence",
                     "Defense Evasion","Discovery","Collection","ML Attack Staging","Exfiltration","Impact", "Privilege Escalation",
                     "Credential Access","Lateral Movement","Command and Control"]
    valid_risk = ["low","medium","high","critical"]
    valid_fidelity = ["low","medium","high"]
    valid_os = ["windows","linux","mac"]
    files = []
    for root, dir, f in os.walk("command_data"):
        for i in f:
            p = os.path.join(root, i)
            files.append(p)
    client = pymongo.MongoClient()
    db = client.malcommands_dev
    command_collection = db.command_collection
    technique_collection = db.technique_collection
    tool_collection = db.tool_collection
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
                        if not technique in techniques:
                            techniques.append(technique)
                            tech_req = technique_collection.find_one({'technique_id' : technique})
                            techs.append(tech_req)
                if "tool" in i.keys():
                    if db.tool_collection.count_documents({"tool":i['tool'].lower()}) > 0:
                        filter = {"tool":i['tool'].lower()}
                        s = tool_collection.find_one(filter, {})
                        i["tool_data"] = s
                    else:
                        print(f"ERROR - No Tool!: {i['command']}")
                else:
                    print(f"ERROR - No Tool!: {i['command']}")
                tactics = list(dict.fromkeys(tactics))
                techniques = list(dict.fromkeys(techniques))
                i['mitre_long'] = techs
                i['mitre_tactics'] = tactics
                i['mitre_techniques'] = techniques
                for t in tactics:
                    if not t in valid_tactics:
                        print(f"ERROR Processing TACTIC: {i['command']}")
                if not i['risk'] or not i['risk'].lower() in valid_risk:
                    print(f"ERROR Processing RISK: {i['command']}")
                if not i['fidelity'] or not i['fidelity'].lower() in valid_fidelity:
                    print(f"ERROR Processing FIDELITY: {i['command']}")
                for o in i['os']:
                    if not o.lower() in valid_os:
                        print(f"ERROR Processing OS: {i['command']}")
                for ck in i['killchain']:
                    if not ck in valid_ckc:
                        print(f"ERROR Processing CKC: {i['command']}")
                if db.command_collection.count_documents({"command":i['command']}) > 0:
                    filter = {"command":f"{i['command']}"}
                    record = command_collection.update_one(filter, {"$set":i})
                else:
                    command_collection.insert_one(i)


def main():
    import_to_mongo()

main()