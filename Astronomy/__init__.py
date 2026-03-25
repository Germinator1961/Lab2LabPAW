import ephem
import pytz

# Position for 2165 Tupper
tupper = ephem.Observer()
tupper.lat = '45.49068460938023'
tupper.lon = '-73.58147714232855'
tupper.elev = 56 + 27  # en-ca.topographic-map.com at 2165 Tupper plus 9 floors
tupper.pressure = 1017  # mbars  TODO: Automate with weather site
tupper.temp = -3  # Celsius  TODO: Automate with weather site
magnetic_declination = -13 + 48 / 60    # For Montreal
local_timezone = pytz.timezone("Canada/Eastern")

sun = ephem.Sun()
moon =ephem.Moon()
