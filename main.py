from glob import escape
from urllib import response
from flask import Flask, make_response, redirect, request


app = Flask(__name__)

@app.route("/")
def index():
    #js = "<style> * {background: #00ff00} </style>"  #
    js = request.remote_addr
    response = make_response(redirect("/hello"))
    response.set_cookie("js", js)
    return response

@app.route("/hello")
def hello():
    js = request.cookies.get('js')
    js = escape(js)
    return f"hole {js}"

if __name__ == "__main__":
    app.run(port = 8080, debug = True)