# Modified from Lab2Lab260314 to work in pythonanywhere account
from datetime import datetime
from os import path
from models import User
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from models import db
from werkzeug.security import check_password_hash, generate_password_hash

from NetworkTools.NetworkTools import get_local_ip, get_public_ip
from Astronomy.Astronomy import get_sunrise, get_sunset, get_sun_azimuth_altitude, tupper, convert_decimal_time, get_moon_graph_data
from Astronomy.Astronomy import get_moon_azimuth_altitude
from Meteo.OpenMeteo import get_weather_data
import ephem
import json

DB_NAME = "l2l.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'  # TODO: Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True

db.init_app(app)
if not path.exists(DB_NAME):
    print('IN CREATE DB')
    with app.app_context():
        db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    aware_datetime = datetime.now().astimezone()
    home_page_variables = {}
    home_page_variables.update({'local_time': aware_datetime.strftime("%H:%M")})
    home_page_variables.update({'today_date': aware_datetime.strftime("%H/%m/%d")})

    home_page_variables.update({'local_ip': get_local_ip()})
    home_page_variables.update({'public_ip': get_public_ip()})

    home_page_variables.update({'sunrise': convert_decimal_time(get_sunrise(tupper, ephem.now()))})
    home_page_variables.update({'sunset': convert_decimal_time(get_sunset(tupper, ephem.now()))})
    saz, sal = get_sun_azimuth_altitude(tupper)
    home_page_variables.update({'sun_azimuth': f"{saz:.2f}"})
    home_page_variables.update({'sun_altitude': f"{sal:.2f}"})

    maz, mal = get_moon_azimuth_altitude(tupper)
    home_page_variables.update({'moon_azimuth': f"{maz:.2f}"})
    home_page_variables.update({'moon_altitude': f"{mal:.2f}"})
    moon_data = get_moon_graph_data(tupper)

    meteo_data = get_weather_data()
    home_page_variables.update({'temperature': meteo_data['temperature_2m']})
    home_page_variables.update({'humidity': meteo_data['relative_humidity_2m']})
    home_page_variables.update({'pressure': meteo_data['pressure_msl']})
    home_page_variables.update({'code': meteo_data['weather_code']})

    return render_template('index.html', title='Home', **home_page_variables, data=json.dumps(moon_data))

@app.route('/about')
def about():
    now = datetime.now()
    home_page_variables = {}
    home_page_variables.update({'local_time': now.strftime("%H:%M")})
    meteo_data = get_weather_data()
    home_page_variables.update({'temperature': meteo_data['temperature_2m']})
    home_page_variables.update({'humidity': meteo_data['relative_humidity_2m']})
    home_page_variables.update({'pressure': meteo_data['pressure_msl']})
    home_page_variables.update({'code': meteo_data['weather_code']})
    return render_template('about.html', title='About', **home_page_variables)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('views.profile'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('profile.login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


if __name__ == '__main__':
    print("IN IF NAME MAIN")
    app.run()
