# DSC510
# Week 12
# Programming Assignment Final Project
# Author Michael Paris
# 10/13/2020

# This program reports current weather information to the user based on their zip code or city/state input
# Weather information is pulled from OpenWeatherMap

# Change Control Log

# Initial Creation
# Date 10/13/2020
# Author: Michael Paris

# Change #1
# Date 10/18/2020
# Author Michael Paris
# added geopy for Lat Long calculations
# added latlonglookup function to calculate lat long from zip or city name
# updated openweather 'One API' call vs. using multiple different APIs
# changed size of UI to better handle the display of the weather data
# added menu item to UI with an Exit command that closes the app

# Change #3
# Date 10/18/2020
# Author Michael Paris
# added classes to model the weatherservice calls and weather

# Change #4
# Date Multiple
# Author Michael Paris
# added weather icons to the display
# updated formatting of GUI to better display (changed to .grid from .pack to better place items)
# added frames to the GUI to better display objects on screen
# added skycode and weathericon to weather class
# added compassheading function to convert wind degrees to a written direction - North, South, etc
# commented the converttime function as it's not needed anymore

# Change #5
# Date 11/20/2020
# changed GUI objects from Tkinter to TTK to allow for a little better looking GUI
# moved weather icons to the same directory as the .py file to keep from using a full absolute file path to them
# added forecast lows and highs


import requests
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from geopy import Nominatim
from datetime import datetime


# weatherservice class to model the calls to openweather API
class WeatherService:
    def __init__(self):
        self.api_key = '0625f47f0c05077a6e6274069444c78c'
        self.current_weather_api = 'https://api.openweathermap.org/data/2.5/weather?'
        self.api_one_call = 'https://api.openweathermap.org/data/2.5/onecall?'
        self.country_code = 'US'
        self.latlong = {}
        self.request = ''
        self.weatherjson = ''

    def latlonglookup(self, arg):
        geolocator = Nominatim(user_agent='weather')
        location = geolocator.geocode(arg)
        lat = location.latitude
        long = location.longitude
        return [lat, long]

    def getforecast(self, location, unit):
        try:
            self.latlong = self.latlonglookup(location)
            self.request = requests.get(self.api_one_call + 'lat=' + str(self.latlong[0]) + '&lon=' +
                                        str(self.latlong[1]) + '&units=' + unit + '&exclude=minutely,'
                                                               'hourly,alerts&appid='
                                        + self.api_key)
            # print(self.request.json())
            # self.request_json = self.request.json()
            # result_temp.insert(INSERT, self.request_json['current']['temp'])
            self.weatherjson = self.request.json()

        except ConnectionError as connection_error:
            print(connection_error)

    def getweatherjson(self):
        return self.weatherjson


# model what the weather is and what it can do, not exactly how it does it, put that in a weather service
class Weather:
    def __init__(self):
        self.lat = ''
        self.long = ''
        self.timezone = ''
        self.timezone_offset = ''
        self.current = ''
        self.sunrise = ''
        self.sunset = ''
        self.temp = ''
        self.feels_like = ''
        self.dewpoint = ''
        self.humidity = 0.0
        self.windspeed = ''
        self.wind_deg = ''
        self.skies = ''
        self.skycode = ''
        self.weathericon = ''
        self.forecast0 = {}
        self.forecast1 = {}
        self.forecast2 = {}
        self.forecast3 = {}
        self.forecast4 = {}

    def setlat(self, arg):
        self.lat = arg

    def getlat(self):
        return self.lat

    def setlong(self, arg):
        self.long = arg

    def getlong(self):
        return self.long

    def settimezone(self, arg):
        self.timezone = arg

    def gettimezone(self):
        return self.timezone

    def settimezone_offset(self, arg):
        self.timezone_offset = arg

    def gettimezone_offset(self):
        return self.timezone_offset

    def setcurrent(self, arg):
        self.current = arg

    def getcurrent(self):
        return self.current

    def setsunrise(self, arg):
        self.sunrise = arg

    def getsunrise(self):
        return self.sunrise

    def setsunset(self, arg):
        self.sunset = arg

    def getsunset(self):
        return self.sunset

    def settemp(self, arg):
        self.temp = arg

    def gettemp(self):
        return self.temp

    def setfeels_like(self, arg):
        self.feels_like = arg

    def getfeels_like(self):
        return self.feels_like

    def setdewpoint(self, arg):
        self.dewpoint = arg

    def getdewpoint(self):
        return self.dewpoint

    def sethumidity(self, arg):
        self.humidity = arg

    def gethumidity(self):
        return self.humidity

    def setwindspeed(self, arg):
        self.windspeed = arg

    def getwindspeed(self):
        return self.windspeed

    def setwind_deg(self, arg):
        self.wind_deg = arg

    def getwind_deg(self):
        return self.wind_deg

    def setskies(self, arg):
        self.skies = arg

    def getskies(self):
        return self.skies

    def setskycode(self, arg):
        self.skycode = arg

    def getskycode(self):
        return self.skycode

    def setweathericon(self, arg):
        self.weathericon = arg

    def getweathericon(self):
        return self.weathericon

    def setforecast0(self, key, value):
        self.forecast0[key] = value

    def getforecast0(self):
        return self.forecast0

    def setforecast1(self, key, value):
        self.forecast1[key] = value

    def getforecast1(self):
        return self.forecast1

    def setforecast2(self, key, value):
        self.forecast2[key] = value

    def getforecast2(self):
        return self.forecast2

    def setforecast3(self, key, value):
        self.forecast3[key] = value

    def getforecast3(self):
        return self.forecast3

    def setforecast4(self, key, value):
        self.forecast4[key] = value

    def getforecast4(self):
        return self.forecast4


# I don't like how complicated these checks have become, refactor this to make the checks more efficient
def deciderequest():
    localweather = WeatherService()

    if len(zip_code_entry.get()) != 0 and len(city_entry.get()) != 0:
        errormessage("Please select a city and state or a Zip Code")
    elif len(zip_code_entry.get()) != 0:
        if len(zip_code_entry.get()) != 5 or not str(zip_code_entry.get().isdigit()):
            errormessage("Zip Codes must be 5 digits long.")
        else:
            localweather.getforecast(zip_code_entry.get() + " " + state_combo.get(), str(unit_option.get()))
            parsejson(localweather.getweatherjson())
    elif len(city_entry.get()) != 0:
        if state_combo.get() == '':
            errormessage("Please select a state.")
        else:
            localweather.getforecast(city_entry.get() + " " + state_combo.get(), str(unit_option.get()))
            parsejson(localweather.getweatherjson())
    else:
        errormessage("Please enter a zip or city and state")

# display a pop-up error message for the user
def errormessage(message):
    mb.showwarning(title="Weather Service", message=message)


# change temp from kelvin to F.
# not needed as API has an argument for imperial, metric, standard
def converttemp(temp):
    temp = temp * 9 / 5 - 459.67
    temp = round(temp, 2)
    return temp


# convert time from UST to time for the forecasted area
def converttime(time):
    return datetime.fromtimestamp(time)


# read in the compass heading for the wind direction and change it to something the user can read
def compassheading(degree):
    if degree > 337.5:
        return 'North'
    elif degree > 292.5:
        return 'North West'
    elif degree > 247.5:
        return 'West'
    elif degree > 202.5:
        return 'South West'
    elif degree > 157.5:
        return 'South'
    elif degree > 122.5:
        return 'South East'
    elif degree > 67.5:
        return 'East'
    elif degree > 22.5:
        return 'North East'
    else:
        return 'Northerly'


# parse the json file and set the weather classes parameters
def parsejson(json):
    weatherresults = Weather()
    weatherresults.setlat(json['lat'])
    weatherresults.setlong(json['lon'])
    weatherresults.settimezone(json['timezone'])
    weatherresults.settimezone_offset(json['timezone_offset'])
    weatherresults.setsunrise(json['current']['sunrise'])
    weatherresults.setsunset(json['current']['sunset'])
    weatherresults.settemp(json['current']['temp'])
    weatherresults.setfeels_like(json['current']['feels_like'])
    weatherresults.setdewpoint(json['current']['dew_point'])
    weatherresults.sethumidity(json['current']['humidity'])
    weatherresults.setwindspeed(json['current']['wind_speed'])
    weatherresults.setwind_deg(json['current']['wind_deg'])
    weatherresults.setskycode(json['current']['weather'][0]['id'])
    weatherresults.setskies(json['current']['weather'][0]['description'])
    weatherresults.setweathericon(json['current']['weather'][0]['icon'])
    for i in range(5):
        getforecast(weatherresults, json, i)
    prettyprint(weatherresults)


# need to find a better way to do this, too much duplication of code
def getforecast(forecast, json, day):
    if day == 0:
        forecast.setforecast0('date', json['daily'][0]['dt'])
        forecast.setforecast0('min', json['daily'][0]['temp']['min'])
        forecast.setforecast0('max', json['daily'][0]['temp']['max'])
    elif day == 1:
        forecast.setforecast1('date', json['daily'][1]['dt'])
        forecast.setforecast1('min', json['daily'][1]['temp']['min'])
        forecast.setforecast1('max', json['daily'][1]['temp']['max'])
    elif day == 2:
        forecast.setforecast2('date', json['daily'][2]['dt'])
        forecast.setforecast2('min', json['daily'][2]['temp']['min'])
        forecast.setforecast2('max', json['daily'][2]['temp']['max'])
    elif day == 3:
        forecast.setforecast3('date', json['daily'][3]['dt'])
        forecast.setforecast3('min', json['daily'][3]['temp']['min'])
        forecast.setforecast3('max', json['daily'][3]['temp']['max'])
    elif day == 4:
        forecast.setforecast4('date', json['daily'][4]['dt'])
        forecast.setforecast4('min', json['daily'][4]['temp']['min'])
        forecast.setforecast4('max', json['daily'][4]['temp']['max'])

# get the current weather and put it into the text box
# change this to format?
def prettyprint(weather_object):
    current_weather.delete('1.0', END)

    # I started to change this to use the .format function, but thought this was easier to read
    weather = "\n".format(width=100) \
              + "{:<50} {}\n".format('Current Weather', 'Forecast', width=100) \
              + "Lat/long: {} / {:<32} {}\n".format(str(weather_object.getlat()), str(weather_object.getlong()), converttime(weather_object.getforecast0().get('date')), width=100) \
              + "Timezone: {:<40} Low: {}\n".format(str(weather_object.gettimezone()), str(weather_object.getforecast0().get('min')), width=100) \
              + "Current Temp: {:<36} High: {}\n".format(str(weather_object.gettemp()), str(weather_object.getforecast0().get('max')), width=100) \
              + "Feels Like: {}\n".format(str(weather_object.getfeels_like()), width=100) \
              + "{} {:<39} {}\n".format('Dew Point:', str(weather_object.getdewpoint()), converttime(weather_object.getforecast1().get('date')), width=100) \
              + "Sunrise: {:<41} Low: {}\n".format(str(converttime(weather_object.getsunrise())), str(weather_object.getforecast1().get('min')), width=100) \
              + "Sunset: {:<42} High: {}\n".format(str(converttime(weather_object.getsunset())), str(weather_object.getforecast1().get('max')), width=100) \
              + "Humidity: {0:.2f}%\n".format(weather_object.gethumidity(), width=100) \
              + "Wind: {:<44} {}\n".format(str(weather_object.getwindspeed()), converttime(weather_object.getforecast2().get('date')), width=100) \
              + "Skies: {:<42}  Low: {}\n".format(str(weather_object.getskies()), str(weather_object.getforecast2().get('min')), width=100) \
              + "{:<50} High: {}\n".format(" ", str(weather_object.getforecast2().get('max')), width=100) \
              + "\n".format(width=100) \
              + "{:<50} {}\n".format(" ", converttime(weather_object.getforecast3().get('date')), width=100) \
              + "{:<50} Low: {}\n".format(" ", str(weather_object.getforecast3().get('min')), width=100) \
              + "{:<50} High: {}\n".format(" ", str(weather_object.getforecast3().get('max')), width=100) \
              + "\n".format(width=100) \
              + "{:<50} {}\n".format(" ", converttime(weather_object.getforecast4().get('date')), width=100) \
              + "{:<50} Low: {}\n".format(" ", str(weather_object.getforecast4().get('min')), width=100) \
              + "{:<50} High: {}\n".format(" ", str(weather_object.getforecast4().get('max')), width=100) \


    sky_code = weather_object.getskycode()
    current_weather.insert(INSERT, "")
    cursor_position = current_weather.index(INSERT)
    current_weather.image_create(cursor_position, image=changeweathericon(sky_code))
    current_weather.insert(INSERT, weather)



# I'd like to put the gui into a class, but had some troubles getting it figured out.
# Will be something I come back and do
app = Tk()
app.title("Weather Reports")
app.geometry("700x700")
states = ['Alabama - AL',
          'Alaska - AK',
          'Arizona - AZ',
          'Arkansas - AR',
          'California - CA',
          'Colorado - CO',
          'Connecticut - CT',
          'Delaware - DE',
          'Florida - FL',
          'Georgia - GA',
          'Hawaii - HI',
          'Idaho - ID',
          'Illinois - IL',
          'Indiana - IN',
          'Iowa - IA',
          'Kansas - KS',
          'Kentucky - KY',
          'Louisiana - LA',
          'Maine - ME',
          'Maryland - MD',
          'Massachusetts - MA',
          'Michigan - MI',
          'Minnesota - MN',
          'Mississippi - MS',
          'Missouri - MO',
          'Montana - MT',
          'Nebraska - NE',
          'Nevada - NV',
          'New Hampshire - NH',
          'New Jersey - NJ',
          'New Mexico - NM',
          'New York - NY',
          'North Carolina - NC',
          'North Dakota - ND',
          'Ohio - OH',
          'Oklahoma - OK',
          'Oregon - OR',
          'Pennsylvania - PA',
          'Rhode Island - RI',
          'South Carolina - SC',
          'South Dakota - SD',
          'Tennessee - TN',
          'Texas - TX',
          'Utah - UT',
          'Vermont - VT',
          'Virginia - VA',
          'Washington - WA',
          'West Virginia - WV',
          'Wisconsin - WI',
          'Wyoming - WY']

sunny = PhotoImage(file="sunny.png").subsample(4, 4)
cloudy = PhotoImage(file="cloudy.png").subsample(4, 4)
rainy = PhotoImage(file="rainy.png").subsample(4, 4)
snowy = PhotoImage(file="snowy.png").subsample(4, 4)
thunderstorm = PhotoImage(file="thunderstorm.png").subsample(4, 4)
misty = PhotoImage(file="misty.png").subsample(4, 4)

# sunny = PhotoImage(file="C:\\Users\\mpari\\OneDrive\\DSC510\\week12\\assignment12.1\\icons\\sunny.png").subsample(3, 3)
# cloudy = PhotoImage(file="C:\\Users\\mpari\\OneDrive\\DSC510\\week12\\assignment12.1\\icons\\cloudy.png").subsample(3, 3)
# rainy = PhotoImage(file="C:\\Users\\mpari\\OneDrive\\DSC510\\week12\\assignment12.1\\icons\\rainy.png").subsample(3, 3)
# snowy = PhotoImage(file="C:\\Users\\mpari\\OneDrive\\DSC510\\week12\\assignment12.1\\icons\\snowy.png").subsample(3, 3)
# thunderstorm = PhotoImage(file="C:\\Users\\mpari\\OneDrive\\DSC510\\week12\\assignment12.1\\icons\\thunderstorm.png").subsample(3, 3)
# misty = PhotoImage(file="C:\\Users\\mpari\\OneDrive\\DSC510\\week12\\assignment12.1\\icons\\misty.png").subsample(3, 3)


# refactor this to pull the icon from openweather API.  Already pulling the icon code, just need to learn how
# to display that icon
def changeweathericon(code):
    weathericon = ''
    if 801 <= code <= 804:
        weathericon = cloudy
    elif code == 800:
        weathericon = sunny
    elif 600 <= code <= 622:
        weathericon = snowy
    elif (500 <= code <= 531) or (300 <= code <= 321):
        weathericon = rainy
    elif code == 701:
        weathericon = misty
    elif 200 <= code <= 232:
        weathericon = thunderstorm
    return weathericon


menu = Menu(app)
menu_item = Menu(menu)
menu_item.add_command(label='Exit', command=app.quit)
menu.add_cascade(label='File', menu=menu_item)
app.config(menu=menu)

search_frame = ttk.LabelFrame(app)
search_frame.grid(row=0, column=0)

option_frame = ttk.LabelFrame(app)
option_frame.grid(row=0, column=1)

icon_frame = ttk.LabelFrame(app)
icon_frame.grid(row=0, column=2)

search_button_frame = ttk.LabelFrame(app)
search_button_frame.grid(row=1, column=0)

result_frame = ttk.LabelFrame(app)
result_frame.grid(row=2, columnspan=2)

weather_icon = ttk.Label(icon_frame)

search_type_label = ttk.Label(search_frame, text="Search Type")
search_type_label.grid(row=0, column=0)

zip_code_label = ttk.Label(search_frame, text="ZipCode")
zip_code_label.grid(row=1, column=0)

zip_code_entry = ttk.Entry(search_frame)
zip_code_entry.grid(row=1, column=1)

city_label = ttk.Label(search_frame, text="City")
city_label.grid(row=2, column=0)

city_entry = ttk.Entry(search_frame)
city_entry.grid(row=2, column=1)

state_label = ttk.Label(search_frame, text="State")
state_label.grid(row=3, column=0)

state_combo = ttk.Combobox(search_frame, state='readonly', values=states)
state_combo.grid(row=3, column=1)

unit_option = tk.StringVar()
unit_option.set('Imperial')

imperial_button = ttk.Radiobutton(option_frame, text='Imperial', variable=unit_option, value='Imperial')
metric_button = ttk.Radiobutton(option_frame, text='Metric', variable=unit_option, value='Metric')
standard_button = ttk.Radiobutton(option_frame, text='Standard', variable=unit_option, value='Standard')

imperial_button.grid(row=1, column=2)
metric_button.grid(row=2, column=2)
standard_button.grid(row=3, column=2)

current_weather = Text(result_frame, height=40)
current_weather.grid(row=0, column=0)

# forecast = Text(result_frame)
# forecast.grid(row=0, column=1)


submit_button = ttk.Button(search_button_frame, text="Submit", command=deciderequest)
submit_button.pack()

app.mainloop()
