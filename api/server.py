import random

import flask
import datetime
from flask import Flask, send_from_directory

app = flask.Flask(__name__)
app.config["DEBUG"]=True

residents = [
    # Enfants
    {"id": 1, "prenom": "Léa", "age": 5, "date_arrivee": "2023-09-20"},
    {"id": 2, "prenom": "Noah", "age": 10, "date_arrivee": "2023-11-02"},
    {"id": 3, "prenom": "Inès", "age": 7, "date_arrivee": "2025-03-01"},

    # Adolescents
    {"id": 4, "prenom": "Rayane", "age": 15, "date_arrivee": "2024-09-10"},
    {"id": 5, "prenom": "Emma", "age": 18, "date_arrivee": "2023-05-15"},
    {"id": 6, "prenom": "Lucas", "age": 14, "date_arrivee": "2025-01-10"},

    # Jeunes adultes
    {"id": 7, "prenom": "Julien", "age": 22, "date_arrivee": "2023-10-10"},
    {"id": 8, "prenom": "Théo", "age": 26, "date_arrivee": "2024-08-01"},
    {"id": 9, "prenom": "Camille", "age": 29, "date_arrivee": "2022-11-05"},

    # Adultes
    {"id": 10, "prenom": "Sarah", "age": 34, "date_arrivee": "2022-12-12"},
    {"id": 11, "prenom": "Dorian", "age": 45, "date_arrivee": "2023-03-22"},
    {"id": 12, "prenom": "Karim", "age": 51, "date_arrivee": "2025-05-10"},

    # Séniors
    {"id": 13, "prenom": "Françoise", "age": 67, "date_arrivee": "2021-07-08"},
    {"id": 14, "prenom": "Bernard", "age": 78, "date_arrivee": "2023-06-19"},
    {"id": 15, "prenom": "Monique", "age": 88, "date_arrivee": "2024-09-30"},

    # Très âgés
    {"id": 16, "prenom": "Albert", "age": 102, "date_arrivee": "2020-01-01"},
    {"id": 17, "prenom": "Jacqueline", "age": 95, "date_arrivee": "2023-08-08"},
]

cadeaux = [
    {"id": 1, "nom": "peluche", "age_min": 0, "age_max": 7},
    {"id": 2, "nom": "jouet", "age_min": 8, "age_max": 14},
    {"id": 3, "nom": "carte cadeau Steam", "age_min": 15, "age_max": 20},
    {"id": 4, "nom": "carte cadeau restaurant", "age_min": 21, "age_max": 30},
    {"id": 5, "nom": "poêle de cuisine", "age_min": 31, "age_max": 99},
    {"id": 6, "nom": "tapis chauffant", "age_min": 70, "age_max": 90},
    {"id": 7, "nom": "trop vieux pour les cadeaux 😅", "age_min": 100, "age_max": 10000}
]

attributions=[]

@app.route('/')
def home():
    return send_from_directory('../client/html', 'index.html')


# --- ROUTES POUR LES FICHIERS STATIQUES ---
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('../client/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('../client/js', filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('../client/assets', filename)



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
    today = datetime.datetime.now()
    limit = today - datetime.timedelta(days=365)

    for resident in residents:
        try:
            arrival_date = datetime.datetime.strptime(resident["date_arrivee"], "%Y-%m-%d")
        except ValueError:
            continue  # skip si date invalide

        # ✅ Éligible si arrivé il y a 1 an ou plus
        if arrival_date <= limit:
            cadeaux_res = [
                cadeau for cadeau in cadeaux
                if cadeau["age_min"] <= resident["age"] <= cadeau["age_max"]
            ]
            eligible.append({
                "resident": resident,
                "cadeau_associe": cadeaux_res
            })
    return flask.jsonify(eligible)


@app.route('/api/v1/attributions', methods=['POST'])
def post_attributions():
    global attributions

    eligible = flask.json.loads(get_eligible().data.decode("utf8"))
    nouvelles_attributions = []

    for resident in eligible:
        # vérifier si déjà attribué
        deja = next((a for a in attributions if a["resident"]["id"] == resident["resident"]["id"]), None)
        if deja:
            continue

        cadeaux_possibles = resident["cadeau_associe"]
        if cadeaux_possibles:
            cadeau = random.choice(cadeaux_possibles)
            attribution = {
                "resident": resident["resident"],
                "cadeau_associe": cadeau,
                "date_attribution": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            attributions.append(attribution)
            nouvelles_attributions.append(attribution)

    # 🔁 on renvoie tout l'historique des attributions (anciennes + nouvelles)
    return flask.jsonify(attributions)


if __name__== '__main__':
    app.run(port=5050, use_reloader=False)