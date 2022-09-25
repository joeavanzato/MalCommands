from flask import abort, Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

# https://paletton.com/#uid=53w0u0kllllxE6Pv4btbBvda7G-

app = Flask(__name__, template_folder='templates')
client = MongoClient()
db = client.malcommands_dev
command_collection = db.command_collection
technique_collection = db.technique_collection


@app.route('/', methods=['GET'])
def index():
    #commands = command_collection.find({}, {'command': 1, 'tool': 1, 'risk': 1, 'fidelity': 1, '_id': 1})
    commands = command_collection.aggregate([{"$project":{'id': '$_id', 'command': 1, 'tool': 1, 'risk': 1, 'fidelity': 1,'mitre_tactics': 1, 'mitre_techniques': 1}},])
    command_list = []
    for i in commands:
        i['mitre_tactics'] = ', '.join(map(str, i['mitre_tactics']))
        i['mitre_techniques'] = ', '.join(map(str, i['mitre_techniques']))
        command_list.append(i)
    return render_template('index.html', commands=list(command_list))
@app.route('/commands/<obj_id>', methods=['GET'])
def commands(obj_id):
    try:
        object = ObjectId(obj_id)
    except:
        abort(404)
    command = command_collection.find({'_id': object}, {})
    return render_template('command_pop.html', command=list(command))
@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')
@app.route('/contribute', methods=['GET'])
def contribute():
    return render_template('contribute.html')

