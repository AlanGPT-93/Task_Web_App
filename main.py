from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest
from app import create_app
from app.forms import LoginForm
from app.firestore_service import get_users, get_todos
from flask_login import login_required, current_user

app = create_app()

#to_dos = ["do1", "do2", "do3"]

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
   
    return response


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id #session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id = username),
        'username': username
    }

    # users = get_users()

    # for user in users:
    #     print(user.id)
    #     print(user.to_dict()['password'])

    return render_template('hello.html', **context)


if __name__ == "__main__":
    app.run(port = 8080, debug = True)