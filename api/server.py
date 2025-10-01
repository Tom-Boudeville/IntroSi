from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():

@app.route("/add", methods=["POST"])
def add_item():
    return

@app.route("/update/<int:id>", methods=["POST"])
def update_item(id):
    return

@app.route("/delete/<int:id>")
def delete_item(id):
    return


if __name__ == "__main__":
    app.run(debug=True)
