import flask

app = flask.Flask(__name__)
app.config["DEBUG"]=True

residents=[]

resident_validator = {
    "id": {
        "type": int,
    },
    "prenom": {
        "type": str,
    },
    "age": {
        "type": int,
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
        if "format" in resident_validator[key]:
            try:
                datetime.strptime(value, resident_validator[key]["format"])
            except ValueError:
                return False
    return True

@app.route('/',methode=['GET'])
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
    residents.append()








if __name__== '__main__':
    app.run(port=5050, use_relaoder=False)