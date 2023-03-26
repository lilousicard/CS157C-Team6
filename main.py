from models import User

from flask import Flask, request, render_template, flash, session, redirect, url_for
import os
flask_app = Flask(__name__)
flask_app.secret_key = os.urandom(24)


@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)

        if len(username) < 1:
            flash('Your username must be at least one character.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not User(username).register(password):
            flash('Username already exists.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('signUp.html')


@flask_app.route('/login')
def login():
    return render_template('login.html')


def main():
    print("Hello World!")
    flask_app.run(debug=True)



if __name__ == "__main__":
    main()
