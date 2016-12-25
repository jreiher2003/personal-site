import os
import random
from datetime import datetime
import pytz
import requests
from app import app
from flask import render_template, url_for, redirect, jsonify, request 
import config 
from config import BaseConfig 

def header():
    return {"Content-Type": "application/json", "User-Agent": "jreiher2003"}
headers = header()

def get_my_ip():
    return request.remote_addr

def find_my_loc():
    user = get_my_ip()
    if os.environ["APP_SETTINGS"] == 'config.DevelopmentConfig':
        return requests.get("http://ipinfo.io/73.55.103.114").json()
    else:
        return requests.get("http://ipinfo.io/" + user).json()

def find_lon_lat():
    user_loc = find_my_loc()
    lon = user_loc['loc'].split(",")[1]
    lat = user_loc['loc'].split(",")[0]
    return lat, lon

def rand_pic(len_object):
    return random.randint(1,len_object+1)

def quotes():
    quote = requests.get("http://quotes.stormconsultancy.co.uk/quotes.json", headers=headers).json()
    return quote[rand_pic(len(quote))]

def profiles():
    return requests.get("https://api.github.com/users/jreiher2003", headers=headers).json()
profile = profiles()

def find_current_weather(params):
    APIKEY = "APPID="+BaseConfig.OPEN_WEATHER_MAP
    URL = "http://api.openweathermap.org/data/2.5/"
    cur = params
    m = URL + cur + APIKEY
    return requests.get(m, headers=headers).json()

def find_user_weather(lat, lon):
    return find_current_weather("weather?lat=%s&lon=%s&units=imperial&" % (lat,lon))

def find_user_sunset_sunrise(lat,lon):
    local_tz = pytz.timezone("US/Eastern")
    weather = find_user_weather(lat,lon)
    s = weather['sys']['sunset']
    r = weather['sys']['sunrise']
    ss = datetime.fromtimestamp(s).replace(tzinfo=pytz.utc)
    rr = datetime.fromtimestamp(r).replace(tzinfo=pytz.utc)
    sunset = ss.astimezone(pytz.timezone('US/Eastern'))
    sunrise = rr.astimezone(pytz.timezone('US/Eastern'))
    return sunrise,sunset

@app.route('/')
def hello_world():
    user_loc = find_my_loc()
    lat, lon = find_lon_lat()
    user_weather = find_user_weather(lat,lon)
    now_utc = datetime.now(pytz.timezone('UTC'))
    dt = now_utc.astimezone(pytz.timezone('US/Eastern'))
    sunrise,sunset = find_user_sunset_sunrise(lat,lon)  
    print sunset 
    quote = quotes()
    return render_template(
        "index.html",
        dt = dt, 
        profile=profile, 
        quote=quote,
        sunrise=sunrise,
        sunset=sunset,
        user_loc=user_loc,
        user_weather=user_weather
        )

@app.route("/projects")
def projects():
    quote = quotes()
    puppy = requests.get("https://api.github.com/repos/jreiher2003/Puppy-Adoption", headers=headers).json()
    portfolio = requests.get("https://api.github.com/repos/jreiher2003/Jeff-Portfolio", headers=headers).json()
    wiki = requests.get("https://api.github.com/repos/jreiher2003/Wiki", headers=headers).json()
    composite = requests.get("https://api.github.com/repos/jreiher2003/Composite", headers=headers).json()
    return render_template(
        "projects.html",
        puppy=puppy,
        portfolio=portfolio,
        wiki=wiki,
        composite=composite,
        quote = quote
        )

@app.route("/resume")
def show_resume():
    return render_template(
        "JeffreyReiherResume.html"
        )



