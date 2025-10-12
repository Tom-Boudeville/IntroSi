import random

import flask
from flask import jsonify
import datetime

app = flask.Flask(__name__)
app.config["DEBUG"]=True

residents=[
    {
        "age": 20,
        "date_arrivee": "2025-10-12",
        "id": 1,
        "prenom": "Julien"
    },
    {
        "age": 130,
        "date_arrivee": "2025-10-12",
        "id": 2,
        "prenom": "Dorian"
    },
    {
        "age": 8,
        "date_arrivee": "2025-10-12",
        "id": 3,
        "prenom": "Rayanne"
    },
    {
        "age": 25,
        "date_arrivee": "1354-10-12",
        "id": 5,
        "prenom": "Theo"
    }]
cadeaux=[{"id":1,"nom":"peluche","age_min":0, "age_max":7},
    {"id":2,"nom":"jouet","age_min":8, "age_max":14},
    {"id":3,"nom":"carte cadeaux steam","age_min":15, "age_max":20},
    {"id": 3, "nom": "carte cadeaux epic", "age_min": 15, "age_max": 20},
    {"id":4,"nom":"carte cadeaux restaurant","age_min":21, "age_max":30 },
    {"id":5,"nom":"poele","age_min":31, "age_max":99},
    {"id":6,"nom":"t'es trop vieux","age_min":100, "age_max":10000}]
attributions=[]

@app.route('/',methods=['GET'])
def home():
    return """<h1> Bienvenue aux nouveaux arrivants</h1>"""



@app.route('/api/v1/residents',methods=['GET'])
def get_residents():
    return flask.jsonify(residents)

@app.route('/api/v1/residents/<int:id>', methods=['GET'])
def get_residents_detail(id):
    resident = next((r for r in residents if r["id"]==id), None)
    if resident is None:
        flask.abort(404, description=f"Résident avec id {id} non trouvé")
    return flask.jsonify(resident)

@app.route('/api/v1/residents', methods=['POST'])
def post_residents():
    resident=flask.json.loads(flask.request.data.decode("utf8"))
    if next((r for r in residents if r["id"]==resident["id"]), False):
        return flask.abort(404,"Le résident existe déjà")
    residents.append(resident)
    return residents

@app.route('/api/v1/residents/<int:id>', methods=['PUT'])
def put_residents(id):
    resident = next((r for r in residents if r["id"]==id), None)
    if resident is None:
        flask.abort(404, description=f"Résident avec id {id} non trouvé")
    data = flask.json.loads(flask.request.data.decode("utf8"))
    resident.update(data)
    return flask.jsonify(resident)

@app.route('/api/v1/residents/<int:id>', methods=['DELETE'])
def delete_resident(id):
    resident = next((r for r in residents if r["id"] == id), None)
    if resident is None:
        flask.abort(404, description=f"Résident avec id {id} non trouvé")
    residents.remove(resident)
    return flask.jsonify({"Resident supprimé": resident})

@app.route('/api/v1/eligible', methods=['GET'])
def get_eligible():
    eligible = []
    for resident in residents:
        if (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")<=resident["date_arrivee"]:
            cadeaux_res=[]
            for cadeau in cadeaux:
                if resident["age"]>= cadeau["age_min"] and resident["age"]<= cadeau["age_max"]:
                    cadeaux_res.append(cadeau)
            eligible.append({"resident": resident, "cadeau_associe": cadeaux_res})
    return flask.jsonify(eligible)

@app.route('/api/v1/attributions', methods=['POST'])
def post_attributions():
    eligible=flask.json.loads(get_eligible().data.decode("utf8"))
    nouvelles_attributions=[]
    for resident in eligible:
        if resident["resident"] not in [a["resident"] for a in attributions if attributions]:
            attributions.append({"resident": resident["resident"], "cadeau_associe": random.choice(resident["cadeau_associe"]), "date_attribution": datetime.datetime.now().strftime("%Y-%m-%d")})
            nouvelles_attributions.append({"resident": resident["resident"], "cadeau_associe": random.choice(resident["cadeau_associe"]), "date_attribution": datetime.datetime.now().strftime("%Y-%m-%d")})
    return flask.jsonify(nouvelles_attributions)



if __name__== '__main__':
    app.run(port=5050, use_reloader=False)