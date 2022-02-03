from crypt import methods
from flask import Flask, render_template, request

app = Flask(__name__)

SPORTS = [
    "Surf",
    "Football",
    "Calisthenics",
    "Scuba Diving",
    "Golf"
]

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/register", methods=["POST"])
def register():
    #Validating submission
    if not request.form.get("name") or request.form.get("sport") not in SPORTS:
        return render_template("failure.html")

    #Confirm registration
    return render_template("success.html")
    