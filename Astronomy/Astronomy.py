# By: Germain Tremblay, Feb 2026
# Ref: https://theskylive.com/moonrise-moonset-times?geoid=6077265
# Ref: pyephem

from Astronomy import tupper, sun, moon, local_timezone
import pytz
import datetime
import ephem
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mydates
import matplotlib.ticker as myticker

def get_sunrise(observer, date):
    observer.date = date
    sun.compute(observer)
    previous_sunrise = observer.previous_rising(sun)
    sr = pytz.utc.localize(previous_sunrise.datetime()).astimezone(local_timezone)
    return sr.hour + sr.minute / 60.0

def get_sunset(observer, date):
    observer.date = date
    sun.compute(observer)
    next_sunset = observer.next_setting(sun)
    ss = pytz.utc.localize(next_sunset.datetime()).astimezone(local_timezone)
    return ss.hour + ss.minute / 60.0

def get_sun_azimuth_altitude(location):
    sun.compute(location)
    return math.degrees(sun.az), math.degrees(sun.alt)

def get_sunrises(start_date, end_date):
    date1 = ephem.date(start_date)
    date2 = ephem.date(end_date)
    rises = []
    for i in range(int(date2-date1)+1):
        rises.append(get_sunrise(i))
    return rises

def get_sunsets(start_date, end_date):
    date1 = ephem.date(start_date)
    date2 = ephem.date(end_date)
    sunsets = []
    for i in range(int(date2-date1)+1):
        current_date = date1 + i
        tupper.date = current_date
        sun.compute(tupper)
        next_sunset = tupper.next_setting(sun)
        ss = pytz.utc.localize(next_sunset.datetime()).astimezone(local_timezone)
        sunsets.append(ss.hour + ss.minute / 60.0)
    return sunsets

def generate_sunrise_sunset_plot(observer, start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    risings = get_sunrises(tupper, start_date, end_date)
    settings = get_sunsets(tupper, start_date, end_date)
    fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')

    ax.set_title("Levés / Couchers du soleil TUPPER 2026")
    ax.set_ylabel('Levés du soleil', color='orange')
    ax.yaxis.set_major_formatter(myticker.FuncFormatter(convert_decimal_time))
    ax.xaxis.set_major_formatter(mydates.DateFormatter('%b-%d'))
    ax.xaxis.set_major_locator(myticker.MaxNLocator(nbins=12))
    ax.plot(dates, risings, color='orange', label='Levés')
    ax.tick_params(axis='x', labelcolor='black', rotation=90)
    ax.grid(True)

    ax2 = ax.twinx()
    ax2.set_ylabel('Couchers du soleil', color='blue')
    ax2.plot(dates, settings, color='blue', label='Couchers')
    ax2.yaxis.set_major_formatter(myticker.FuncFormatter(convert_decimal_time))
    ax2.tick_params(axis='y', labelcolor='blue')

    plt.show()

def convert_decimal_time(x, pos=None):
    h = int(x)
    m = int((x - h) * 60)
    return f"{h:02d}:{m:02d}"

def generate_analemma(location, start_date_time):
    date1 = ephem.date(start_date_time)
    altitudes = []
    azimuths = []
    for i in range(365):
        location.date = date1
        sun.compute(location)
        alt, azi = get_sun_azimuth_altitude(location)
        altitudes.append(alt)
        azimuths.append(azi)
        date1 += 1
    return altitudes, azimuths

def generate_analemma_plot(location):
    #obs_time = ephem.now()
    # Noon time is 5 hours more in Montreal
    al12, az12 = generate_analemma(location, '2026/01/01 17:00:00')
    al8, az8 = generate_analemma(location, '2026/01/01 13:00:00')
    al10, az10 = generate_analemma(location, '2026/01/01 15:00:00')
    al14, az14 = generate_analemma(location, '2026/01/01 19:00:00')
    al16, az16 = generate_analemma(location, '2026/01/01 21:00:00')

    plt.scatter(al12, az12, color='black', label='12:00', s=1)
    plt.scatter(al8, az8, color='red', label='08:00', s=1)
    plt.scatter(al10, az10, color='orange', label='10:00', s=1)
    plt.scatter(al14, az14, color='green', label='14:00', s=1)
    plt.scatter(al16, az16, color='blue', label='16:00', s=1)

    plt.xlabel('Azimuth')
    plt.ylabel('Altitude')
    plt.title('Analemma for Tupper')
    plt.legend()
    plt.grid(color='gray', linestyle='--', linewidth=1, alpha=0.6)
    plt.show()

def get_moon_azimuth_altitude(location):
    moon.compute(location)
    return math.degrees(moon.az), math.degrees(moon.alt)

def get_moon_graph_data(location):
    moon_data = {}
    utc_time = ephem.now()
    location.date = utc_time
    lt = ephem.localtime(utc_time)
    noon = datetime.datetime(lt.year, lt.month, lt.day, 12, 0, 0)
    time_difference = lt-noon
    moon_data['delta_noon'] = time_difference.total_seconds()/60   # Delta in minutes

    fhour_now = lt.strftime("%H:%M")    # Formatted time
    fdate_now = lt.strftime("%Y/%m/%d")  # Formatted date
    moon_data['date'] = fdate_now
    moon_data['hour'] = fhour_now

    transit1 = location.previous_transit(moon)
    transit1_local = ephem.localtime(transit1)
    ftransit1_local = transit1_local.strftime("%H:%M")
    moon_data['transit1'] = ftransit1_local
    moon_data['dt1'] = (transit1 - utc_time) * 24 * 60   # Delta in minutes

    transit2 = location.next_transit(moon)
    transit2_local = ephem.localtime(transit2)
    ftransit2_local = transit2_local.strftime("%H:%M")
    moon_data['transit2'] = ftransit2_local
    moon_data['dt2'] = (transit2 - utc_time) * 24 * 60   # Delta in minutes

    location.date = transit1
    rise1 = location.previous_rising(moon)
    rise1_local = ephem.localtime(rise1)
    moon_data['rise1'] = rise1_local.strftime("%H:%M")
    moon_data['dr1'] = (rise1 - utc_time) *24 *60

    set1 = location.next_setting(moon)
    set1_local = ephem.localtime(set1)
    moon_data['set1'] = set1_local.strftime("%H:%M")
    moon_data['ds1'] = (set1 - utc_time) * 24 * 60

    location.date = transit2
    rise2 = location.previous_rising(moon)
    rise2_local = ephem.localtime(rise2)
    moon_data['rise2'] = rise2_local.strftime("%H:%M")
    moon_data['dr2'] = (rise2 - utc_time) * 24 * 60

    set2 = location.next_setting(moon)
    set2_local = ephem.localtime(set2)
    moon_data['set2'] = set2_local.strftime("%H:%M")
    moon_data['ds2'] = (set2 - utc_time) * 24 * 60

    return moon_data

'''
print(f"Moon Right Ascension (a_ra): {moon.a_ra}")
print(f"Moon Declination (a_dec): {moon.a_dec}")
print(f"Moon Phase (illumination %): {moon.moon_phase * 100:.2f}%")
print(f"Distance to Moon (range): {moon.earth_distance*ephem.meters_per_au/1000} km")  # distance from observer
print(f"Next Moonrise: {tupper.next_rising(moon)}")
print(f"Next Moon set: {tupper.next_setting(moon)}")
# Convert radians to degrees for RA/Dec if needed
print("-" * 30)
print(f"Moon Right Ascension (degrees): {math.degrees(moon.a_ra):.4f}")
print(f"Moon Declination (degrees): {math.degrees(moon.a_dec):.4f}")
'''
