# Modified from Lab2Lab260314 to work in pythonanywhere account
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    #tz = ZoneInfo("America/Montreal")
    #aware_datetime = datetime.now(tz)
    #home_page_variables = {}
    #home_page_variables.update({'local_time': aware_datetime.strftime("%H:%M")})
    #home_page_variables.update({'today_date': aware_datetime.strftime("%H/%m/%d")})

    #home_page_variables.update({'local_ip': get_local_ip()})
    #home_page_variables.update({'public_ip': get_public_ip()})

    #home_page_variables.update({'sunrise': convert_decimal_time(get_sunrise(tupper, ephem.now()))})
    #home_page_variables.update({'sunset': convert_decimal_time(get_sunset(tupper, ephem.now()))})
    #saz, sal = get_sun_azimuth_altitude(tupper)
    #home_page_variables.update({'sun_azimuth': f"{saz:.2f}"})
    #home_page_variables.update({'sun_altitude': f"{sal:.2f}"})

    #maz, mal = get_moon_azimuth_altitude(tupper)
    #home_page_variables.update({'moon_azimuth': f"{maz:.2f}"})
    #home_page_variables.update({'moon_altitude': f"{mal:.2f}"})
    #moon_data = get_moon_graph_data(tupper)

    #meteo_data = get_weather_data()
    #home_page_variables.update({'temperature': meteo_data['temperature_2m']})
    #home_page_variables.update({'humidity': meteo_data['relative_humidity_2m']})
    #home_page_variables.update({'pressure': meteo_data['pressure_msl']})
    #home_page_variables.update({'code': meteo_data['weather_code']})

    #return render_template('index.html', title='Home', **home_page_variables, data=json.dumps(moon_data))
    return "In home lab2lab"

'''
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
'''

'''
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
'''

if __name__ == '__main__':
    print("IN IF NAME MAIN")
    app.run()
