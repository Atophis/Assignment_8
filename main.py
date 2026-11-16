import flask

app = flask.Flask(__name__, static_folder="Assets", static_url_path="/assets")

@app.route("/", methods=['GET','POST'])
def start():
    return flask.redirect("/home")

@app.route("/home", methods=['GET'])
def insert():
    return flask.render_template("homepage.html")

if __name__== "__main__":
    app.run(debug=False)
