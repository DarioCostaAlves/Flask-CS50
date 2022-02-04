# Implements a registration form, confirming registration via email
# Implements a registration form, storing registrants in a SQLite database, with support for deregistration
from cs50 import SQL
from flask import Flask, redirect, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
db = SQL("sqlite:///froshims.db")

#Requires that "Less secure app access" be on
# https://support.google.com/accounts/answer/6010255

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'a7b36ecd3f2cfe'
app.config['MAIL_PASSWORD'] = 'd2e674be4a432c'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


SPORTS = [
    "Calisthenics",
    "Scuba Diving",
    "Football",
    "Surf",
    "Bodyboard"    
]


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/remove", methods=["POST"])
def remove():

    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect("/registrants")


@app.route("/register", methods=["POST"])
def register():

    # Validate submission
    name = request.form.get("name")
    email = request.form.get("email")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")

    # Remember registrant
    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", name, sport)

    #send email
    message = Message(f"You are registered! {sport}", sender='peter@mailtrap.io', recipients=[email])
    mail.send(message)

    # Confirm registration
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    registrants = db.execute("SELECT * FROM registrants")
    return render_template("registrants.html", registrants=registrants)
