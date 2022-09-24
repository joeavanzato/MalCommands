import yaml
import pymongo
import os

def import_to_mongo():
    files = []
    for root, dir, f in os.walk("command_data"):
        for i in f:
            p = os.path.join(root, i)
            files.append(p)
    client = pymongo.MongoClient()
    db = client.malcommands_dev
    command_collection = db.command_collection
    for f in files:
        print(f"Loading: {f}")
        with open(f, 'r') as f:
            data = yaml.safe_load(f)
        if data is not None:
            for i in data:
                if db.command_collection.count_documents({"command":i['command']}) > 0:
                    filter = {"command":f"{i['command']}"}
                    record = command_collection.update_one(filter, {"$set":i})
                else:
                    command_collection.insert_one(i)


def main():
    import_to_mongo()

main()