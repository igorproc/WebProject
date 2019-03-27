from flask import Flask, redirect, session, request
from flask import render_template as flask_render_template
import extra.auth as auth
from forms import *

from models import User


def init_route(app, db):

    def render_template(*args, **kwargs):
        kwargs['auth_user'] = auth.get_user()
        return flask_render_template(*args, **kwargs)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('base.html')

    @app.route('/install')
    def install():
        db.create_all()
        return render_template(
            'install-success.html',
            title="Главная"
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        has_error = False
        login = ''
        if request.method == 'POST':
            username = request.form['username']
            if auth.login(username, request.form['password']):
                return redirect('/')
            else:
                has_error = True
        return render_template(
            'login.html',
            title='Вход',
            login=login,
            has_error=has_error
        )

    @app.route('/logout', methods=['GET'])
    def logout():
        auth.logout()
        return redirect('/')

    @app.route('/user/create', methods=['GET', 'POST'])
    def registration():
        has_error = False
        form = UserCreateForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user:
                has_error = True
            else:
                User.add(username=username, password=password)
                auth.login(username, password)
                return redirect('/')
        return render_template(
            'registration.html',
            title='Зарегистрироваться',
            form=form,
            has_error=has_error
        )
