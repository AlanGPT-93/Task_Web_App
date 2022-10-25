from flask import render_template, session, redirect, flash, url_for

from app.forms import LoginForm

from . import auth
from .. firestore_service import get_user, add_new_user
from .. models import UserData, UserModel
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are logged")
        return redirect(url_for("index") )
    else:
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        if login_form.validate_on_submit():
            username = login_form.username.data
            #session['username'] = username
            password = login_form.password.data

            user_doc = get_user(username).to_dict()

            if user_doc is not None:
                password_from_db = user_doc["password"]

                if password == password_from_db:
                    user_data = UserData(username = username, password = password)
                    user = UserModel(user_data)

                    login_user(user = user)
                    flash("Welcome")
                    redirect(url_for("hello") )
                else:
                    flash("Wrong user")
            else:
                flash("User not found")


            #flash('Nombre de usario registrado con éxito!')

            return redirect(url_for('index'))

        return render_template('login.html', **context)

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            add_new_user(user_data)

            user = UserModel(user_data)

            login_user(user)

            flash('Bienvenido!')

            return redirect(url_for('hello'))

        else:
            flash('El usario existe!')

    return render_template('signup.html', **context)



@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))