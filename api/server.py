import flask

app = flask.Flask(__name__)
app.config["DEBUG"]=True

residents=[]

@app.route('/',methode=['GET'])
def home():
    return """<h1> Bienvenue aux nouveaux arrivants</h1>"""



@app.route('/api/v1/residents',methods=['GET'])
def get_residents():
    return flask.jsonify(residents)

@app.route('/api/v1/residents', methods=['POST'])
def post_residents():
    resident=flask.json.loads(flask.request.data.decode("utf8"))
    if next((r for r in residents if r["id"]==resident["id"]), False):
        return flask.abort(404,"resident already exist")
    residents.append()








if __name__== '__main__':
    app.run(port=5050, use_relaoder=False)