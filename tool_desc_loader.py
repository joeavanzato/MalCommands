import yaml
import pymongo

def import_to_mongo():
    f = "tool_descriptions.yml"
    client = pymongo.MongoClient()
    db = client.malcommands_dev
    tool_collection = db.tool_collection
    print(f"Loading: {f}")
    with open(f, 'r') as f:
        data = yaml.safe_load(f)
    if data is not None:
        for i in data:
            if db.tool_collection.count_documents({"tool":i['tool']}) > 0:
                filter = {"tool":f"{i['tool']}"}
                record = tool_collection.update_one(filter, {"$set":i})
            else:
                tool_collection.insert_one(i)


def main():
    import_to_mongo()

main()