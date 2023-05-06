from Restaurants import Restaurants
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
	rests = Restaurants("")
	restaurants = rests.get_all()
	
	return render_template('home.html', list = restaurants)


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
    curr_user = models.get_customer(session.get('user'))
    user_friends = Customer(session.get('user')).get_num_friends()
    review_list = Customer(session.get('user')).get_review();
    return render_template('account.html', curr_user=curr_user,
                           user_friends=user_friends, review = review_list)


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
        Customer(other_user).add_friend(cur_user)
        return redirect(request.referrer)
    return redirect(url_for('login'))


@flask_app.route('/remove_friend', methods=["GET", "POST"])
def remove_friend():
    # Currently, if a user unfriends someone, they will also be unfriended
    # by the other user
    cur_user = session.get('user')
    other_user = request.form.get('email')
    if cur_user:
        Customer(cur_user).remove_friend(other_user)
        Customer(other_user).remove_friend(cur_user)
        return redirect(request.referrer)
    return redirect(url_for('login'))


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


@flask_app.route('/friendsPage')
def friend_list():
    user = request.args.get('user_friends')
    # if we click the friends button from navbar, there is no form
    # submitting the 'user_friends' information so user will be None,
    # in this case we can just grab the logged-in user
    if user is None:
        user = session.get('user')
    friends = Customer(user).get_friends()
    return render_template('friendsPage.html', user_friend_list=friends)


@flask_app.route('/city')
def city():
    return render_template('city.html')


######### Restaurant specific functions ############

@flask_app.route('/explore')
def explore_restaurants():
    user = session.get('user')
    if user is not None:
        rests = Restaurants("")
        restaurants = rests.get_all()
        restaurants = add_user_prefs(restaurants)
        #restaurants = [{"name": "First"}, {"name": "Second"}]
        return render_template('explore.html', list = restaurants)
    return redirect(url_for('login'))


def add_user_prefs(restaurants):
    user = session.get('user')
    all_liked_restaurants_nodes = Customer(user).get_all_liked_restaurants()
    liked_restaus_list = []
    for x in all_liked_restaurants_nodes:
        liked_restaus_list.append(x.end_node['name'])
    for x in restaurants:
        if x['name'] in liked_restaus_list:
            x['like'] = True
    return restaurants



@flask_app.route('/like_restaus', methods = ["POST"])
def like_restaus():
    user = session.get('user')
    if user is not None:
        if request.method == 'POST':
            if 'like' in request.form:
                r_name = request.form['like']
                Restaurants(r_name).create_like(r_name, user)
            elif 'unlike' in request.form:
                r_name = request.form['unlike']
                Restaurants(r_name).delete_like(r_name, user)

        restaurants = session.get('restaurants')
        # if restaurants is not None:
        #     return render_template('explore.html', list=restaurants)
        # else:
        rests = Restaurants("")
        restaurants = rests.get_all()
        restaurants = add_user_prefs(restaurants)
        session['restaurants'] = restaurants
        return render_template('explore.html', list = restaurants)
    return redirect(url_for('login'))



    # redirect to the same page
    # check if restaurant liked or not


@flask_app.route('/restaurant/review/<name>', methods = ["GET", "POST"])
def review(name):
    user = session.get('user')
    if user is not None:
        if request.method == "POST":
            rating = request.form.get('rating')
            review = request.form.get('review')
            Restaurants(name).store_rating(rating, review, user)

            #redirect to the same restaurant page after processing reviwe
            restau = Restaurants(name).get_all_details()
            return render_template('restaurant.html', restau=restau)
        return render_template('review.html', name=name)
    return redirect(url_for('login'))


@flask_app.route('/restaurant/<name>')
def restaurant(name):
    user = session.get('user')
    restau = Restaurants(name).get_all_details()
    print(restau)
    if user is not None:
        return render_template('restaurant.html', restau = restau)
    return redirect(url_for('login'))


######## Main method ############

def main():
    flask_app.run(port=5001, debug=True)


if __name__ == "__main__":
    main()
