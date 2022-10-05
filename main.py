from ensurepip import bootstrap
from glob import escape
from urllib import response
from flask import Flask, make_response, redirect, request, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__,
static_folder =  "static")

bootstrap = Bootstrap(app)


to_dos = ["do1", "do2", "do3"]

@app.route("/")
def index():
    #js = "<style> * {background: #00ff00} </style>"  #
    user_ip = request.remote_addr
    response = make_response(redirect("/hello"))
    response.set_cookie("user_ip", user_ip)
    return response

@app.route("/hello")
def hello():
    user_ip = request.cookies.get('user_ip')
    #user_ip = escape(user_ip)
    context = {
        "to_dos": to_dos,
        "user_ip": user_ip
    }

    return render_template("hello.html", **context)

if __name__ == "__main__":
    app.run(port = 8080, debug = True)