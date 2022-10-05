from flask import Flask, make_response, redirect, request, render_template, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__, static_folder =  "static")
app.config.update(ENV = "development")
app.config["SECRET_KEY"] = "TOP SECRET"

class LoginForm(FlaskForm):
    username = StringField("User Name", validators = [DataRequired()]) 
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Enviar")

bootstrap = Bootstrap(app)


to_dos = ["do1", "do2", "do3"]

@app.route("/")
def index():
    #js = "<style> * {background: #00ff00} </style>"  #
    user_ip = request.remote_addr
    response = make_response(redirect("/hello"))
    #response.set_cookie("user_ip", user_ip)
    session["user_ip"] = user_ip
    return response

@app.route("/hello")
def hello():
    #user_ip = request.cookies.get('user_ip')
    user_ip = session.get("user_ip")
    login_form = LoginForm()

    context = {
        "to_dos": to_dos,
        "user_ip": user_ip,
        "login_form": login_form
    }

    return render_template("hello.html", **context)

if __name__ == "__main__":
    app.run(port = 8080, debug = True)