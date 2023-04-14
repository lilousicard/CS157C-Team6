import models
from Customer import Customer

from flask import Flask, request, render_template, flash, session,  \
    redirect, url_for

from passlib.hash import bcrypt
import os
flask_app = Flask(__name__)
flask_app.secret_key = os.urandom(24)
flask_app.config['STATIC_FOLDER'] = 'static'


@flask_app.route('/')
def index():
    return render_template('home.html')


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        image = request.files['picture']
        image_path = os.path.join(flask_app.config['STATIC_FOLDER'],
                                  'media', 'profile_pictures', image.filename)
        image.save(image_path)

        email = request.form['email']
        password = request.form['password']
        params = {
            'name': request.form['name'],
            'password': password,
            'gender': request.form['gender'],
            'age': request.form['age'],
            'restaurant_owner': request.form.get('restaurant'),
            'image_path': image_path
        }

        if len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not Customer(email).register(params):
            flash('Username already exists.')
        else:
            session['user'] = email
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('register.html')


@flask_app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')


def home():
    return render_template('home.html')


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not Customer(email).verify_password(password):
            flash('Invalid login.')
            return render_template('login.html', error=True)
        else:
            session['user'] = email
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')


@flask_app.route('/account')
def account():
    curr_user = models.get_customer(session.get('user'))
    return render_template('account.html', curr_user=curr_user)


@flask_app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        category = request.form['search_category']
        search_term = request.form['search_term']

        if search_term:
            results = models.search_node(category, search_term)
            session['results'] = results
            return redirect(url_for('search_results'))

    return render_template('search.html')


@flask_app.route('/search_results', methods=["GET"])
def search_results():
    results = session.get('results')
    customer = Customer(session.get('user'))
    return render_template('search_results.html', results=results, customer=customer)


@flask_app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.')
    return redirect(url_for('index'))


@flask_app.route('/add_friend', methods=["GET", "POST"])
def add_friend():
    cur_user = session['user']
    other_user = request.form['email']
    if cur_user:
        print(f"{cur_user} sending friend request to {other_user}")
        Customer(cur_user).add_friend(other_user)
        return redirect(request.referrer)
    return redirect(url_for('login'))


@flask_app.route('/review')
def review():
    return render_template('review.html')


# should be accessible to only owners
@flask_app.route('/editForm')
def restaurantForm():
    return render_template('restaurantForm.html')


@flask_app.route('/otherProfile', methods=['POST'])
def other_profile():
    email = request.form['email']
    other_user = models.get_customer(email)
    session['user'] = True
    return render_template('otherProfile.html', other_user=other_user)


def main():
    flask_app.run(port=5001, debug=True)


if __name__ == "__main__":
    main()
