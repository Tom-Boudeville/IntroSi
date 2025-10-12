import random

import flask
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
    }
]
cadeaux=[
    {"id":1,"nom":"peluche","age_min":False, "age_max":7},
    {"id":2,"nom":"jouet","age_min":8, "age_max":14},
    {"id":3,"nom":"carte cadeaux steam","age_min":15, "age_max":20},
    {"id":4,"nom":"carte cadeaux epic game","age_min":15, "age_max":20},
    {"id":5,"nom":"carte cadeaux restaurant","age_min":21, "age_max":30 },
    {"id":6,"nom":"carte cadeaux bouygues","age_min":31, "age_max":99},
    {"id":7,"nom":"t'es trop vieux","age_min":100, "age_max":False}
]

attributions = [

]

resident_validator = {
    "id": {
        "type": int,
    },
    "prenom": {
        "type": str,
    },
    "age": {
        "type": int,
        "min": 0,
        "max": 150,
    },
    "date_arrivee": {
        "type": str,
        "format": "%Y-%m-%d"
    }
}

def resident_validate(data):
    for key, value in data.items():
        if key not in resident_validator:
            return False
        if type(value) != resident_validator[key]["type"]:
            return False
        if "min" in resident_validator[key]:
            if value < resident_validator[key]["min"]:
                return False
        if "max" in resident_validator[key]:
           if value > resident_validator[key]["max"]:
               return False
        if "format" in resident_validator[key]:
            try:
                datetime.datetime.strptime(value, resident_validator[key]["format"])
            except ValueError:
                return False
    return True

@app.route('/',methods=['GET'])
def home():
    return """<h1> Bienvenue aux nouveaux arrivants</h1>"""



@app.route('/api/v1/residents',methods=['GET'])
def get_residents():
    return flask.jsonify(residents)

@app.route('/api/v1/residents', methods=['POST'])
def post_residents():
    resident=flask.json.loads(flask.request.data.decode("utf8"))
    if not resident_validate(resident):
        return flask.abort(400,"bad request")
    if next((r for r in residents if r["id"]==resident["id"]), False):
        return flask.abort(404,"resident already exist")
    residents.append(resident)
    return flask.jsonify(resident)

@app.route('/api/v1/residents/<int:resident_id>', methods=['GET'])
def get_resident(resident_id):
    resident=next((r for r in residents if r["id"]==resident_id), False)
    if not resident:
        return flask.abort(404,"resident not found")
    return flask.jsonify(resident)

@app.route('/api/v1/residents/<int:resident_id>', methods=['PUT'])
def put_resident(resident_id):
    resident = next((r for r in residents if r["id"] == resident_id), False)
    if not resident:
        return flask.abort(404, "resident not found")
    data = flask.json.loads(flask.request.data.decode("utf8"))
    if not resident_validate(data):
        return flask.abort(400, "bad request")
    data.remove("id")
    resident.update(data)
    return flask.jsonify(resident)

@app.route('/api/v1/residents/<int:resident_id>', methods=['DELETE'])
def delete_resident(resident_id):
    resident = next((r for r in residents if r["id"] == resident_id), False)
    if not resident:
        return flask.abort(404, "resident not found")
    residents.remove(resident)
    return flask.jsonify({"success": True, "deleted resident": resident})

@app.route('/api/v1/eligible', methods=['GET'])
def eligibility():
    """
    un resident est eligible s'il est arrivé il y a moins d'un an. Un cadeau lui est attribué en fonction de son âge.
    :return: La liste des habitants eligibles et leur cadeau.
    """
    result = []
    residents_eligible = [r for r in residents if r["date_arrivee"] >= (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")]
    for resident in residents_eligible:
        cadeaux_par_age = [
            c for c in cadeaux
            if (c["age_min"] is False or c["age_min"] <= resident["age"]) and
               (c["age_max"] is False or resident["age"] <= c["age_max"])
        ]
        result.append({"resident": resident, "cadeau_associe": cadeaux_par_age})
    return flask.jsonify(result)

@app.route('/api/v1/attributions', methods=['POST'])
def post_attributions():
    data_eligible = flask.json.loads(eligibility().data.decode("utf8"))
    nouvelle_attributions = []
    for resident in data_eligible:
        if resident["resident"]["id"] not in [a["resident"]["id"] for a in attributions if attributions]:
            cadeaux_par_age = resident["cadeau_associe"]
            if len(cadeaux_par_age) > 0:
                att = {"resident": resident["resident"], "cadeau": random.choice(cadeaux_par_age), "date": datetime.datetime.now().strftime("%Y-%m-%d")}
                attributions.append(att)
                nouvelle_attributions.append(att)
    return flask.jsonify(nouvelle_attributions)

if __name__== '__main__':
    app.run(port=5050, use_reloader=False)