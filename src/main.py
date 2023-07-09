from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    """ index """
    return "Congratulations, it's a web app!"

@app.route("/<pound>")
def main_pound():
    """ runner for POUND workflow """
    return "Pound"

@app.route("/<pomsquad>")
def main_pom():
    """ runner for PomSquad workflow """
    return "PomSquad"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)