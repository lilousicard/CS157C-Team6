from models import Customer

from flask import Flask, request, render_template, flash, session,  \
    redirect, url_for
import os
flask_app = Flask(__name__)
flask_app.secret_key = os.urandom(24)


@flask_app.route('/')
def index():
    return render_template('home.html')


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        params = {
            'password': password,
            'gender': request.form['gender'],
            'email': request.form['email'],
            'age': request.form['age'],
            'restaurant_owner': request.form.get('restaurant')
        }

        if len(username) < 1:
            flash('Your username must be at least one character.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not Customer(username).register(params):
            flash(' Username already exists.')
        else:
            session['user'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('register.html')


@flask_app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')
def home():
    return render_template('home.html')

@flask_app.route('/signup')
def signup():
    return render_template('signup.html')


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        if not Customer(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['user'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')

@flask_app.route('/account')
def account():
    return render_template('account.html')


@flask_app.route('/search')
def search():
    return render_template('search.html')

@flask_app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user', None)
    flash('Logged out.')
    return redirect(url_for('index'))


@flask_app.route('/add_friend', methods=["GET", "POST"])
def add_friend():
    username = session['user']
    Customer(username).add_friend("bob")
    return redirect(url_for('index'))

@flask_app.route('/review')
def review():
    return render_template('review.html')


@flask_app.route('/editForm')
def restaurantForm():
    return render_template('restaurantForm.html')


@flask_app.route('/otherProfile')
def otherPeople():
    return render_template('otherProfile.html')


def main():
    flask_app.run(port=5001, debug=True)


if __name__ == "__main__":
    main()
