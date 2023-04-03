from models import Customer

from flask import Flask, request, render_template, flash, session, redirect, url_for
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
            'username' : username,
            'password' : password,
            'gender' : request.form['gender'],
            'email' : request.form['email'],
            'age' : request.form['age'],
            'restaurant_owner' : request.form.get('restaurant')
        }

        if len(username) < 1:
            flash('Your username must be at least one character.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not Customer(params).register():
            flash(' Username already exists.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('signUp.html')



#*******************************************


@flask_app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')
def home():
    return render_template('home.html')

@flask_app.route('/signup')
def signup():
    return render_template('signup.html')

@flask_app.route('/login')
def login():
    return render_template('login.html')


@flask_app.route('/account')
def account():
    return render_template('account.html')


@flask_app.route('/search')
def search():
    return render_template('search.html')
    
@flask_app.route('/review')
def review():
    return render_template('review.html')

@flask_app.route('/editForm')
def restaurantForm():
    return render_template('restaurantForm.html')

@flask_app.route('/otherProfile')
def otherPeople():
    return render_template('otherProfile.html')

#*******************************************





def main():
    print("Hello World!")
    flask_app.run(port=5001, debug=True)



if __name__ == "__main__":
    main()
