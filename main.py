import models
from Customer import Customer

from flask import Flask, request, render_template, flash, session,  \
    redirect, url_for

from passlib.hash import bcrypt
import os
flask_app = Flask(__name__)
flask_app.secret_key = os.urandom(24)
flask_app.config['STATIC_FOLDER'] = 'static'

# TODO:
# 2. display friend count on profile page
# 3. allow for click on friend count to display and list all friends


@flask_app.route('/')
def index():
    return render_template('home.html')


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        image = request.files.get('picture')
        image_path = os.path.join(flask_app.config['STATIC_FOLDER'],
                                  'media', 'profile_pictures', image.filename)
        image.save(image_path)

        email = request.form.get('email')
        password = request.form.get('password')
        params = {
            'name': request.form.get('name'),
            'password': password,
            'gender': request.form.get('gender'),
            'age': request.form.get('age'),
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
        email = request.form.get('email')
        password = request.form.get('password')
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
    session['user'] = "emilyhunter@gmail.com"
    curr_user = models.get_customer(session.get('user'))
    user_friends = Customer(session.get('user')).get_num_friends()
    return render_template('account.html', curr_user=curr_user,
                           user_friends=user_friends)


@flask_app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        category = request.form['search_category']
        search_term = request.form['search_term']

        if search_term:
            results = models.search_node(category, search_term, session.get(
                'user'))
            session['search_results'] = results
            return redirect(url_for('search_results'))

    return render_template('search.html')


@flask_app.route('/search_results', methods=["GET"])
def search_results():
    results = session.get('search_results')
    customer = Customer(session.get('user'))
    return render_template('search_results.html', results=results,
                           customer=customer)


@flask_app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.')
    return redirect(url_for('index'))


@flask_app.route('/add_friend', methods=["GET", "POST"])
def add_friend():
    # Relationships are not bidirectional, so need to call add friends for
    # both Customer instances
    cur_user = session.get('user')
    other_user = request.form.get('email')
    if cur_user:
        Customer(cur_user).add_friend(other_user)
        # relationships are not bidirectional so make them
        Customer(other_user).add_friend(cur_user)
        return redirect(request.referrer)
    return redirect(url_for('login'))


@flask_app.route('/remove_friend', methods=["GET", "POST"])
def remove_friend():
    # TODO
    # Removing friends will not remove both relationships
    # If we want that to happen then add
    # Customer(other_user).remove_friend(cur_user)
    # so if amy unfriends zach, should zach still be friends with amy?
    cur_user = session.get('user')
    other_user = request.form.get('email')
    if cur_user:
        Customer(cur_user).remove_friend(other_user)
        return redirect(request.referrer)
    return redirect(url_for('login'))


@flask_app.route('/review')
def review():
    return render_template('review.html')


# should be accessible to only owners
@flask_app.route('/editForm')
def restaurant_form():
    return render_template('restaurantForm.html')


@flask_app.route('/otherProfile', methods=["GET", "POST"])
def other_profile():
    email = request.form.get('email')
    if email is None:
        email = session.get('other_profile')
    else:
        session['other_profile'] = email
    other_user = models.get_customer(email)
    customer = Customer(session.get('user'))
    user_friends = Customer(email).get_num_friends()
    return render_template('otherProfile.html', other_user=other_user,
                           customer=customer, user_friends=user_friends)


def main():
    flask_app.run(port=5001, debug=True)


if __name__ == "__main__":
    main()
