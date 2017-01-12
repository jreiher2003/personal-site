import os
import random
import time
from datetime import datetime
import pytz
import requests
from app import app, cache
from flask import render_template, url_for, redirect, jsonify, request 
from user_agents import parse
import googlemaps 
import config 
from config import BaseConfig 

def header():
    return {"Content-Type": "application/json", "User-Agent": "jreiher2003"}
headers = header()

def get_my_ip():
    return request.remote_addr

def degrees_to_cardinal(d):
    '''
    note: this is highly approximate...
    author: RobertSudwarts. githubGist: https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    '''
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((d + 11.25)/22.5)
    return dirs[ix % 16]

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

def find_local_tz():
    """ google maps api for finding local tz """
    epoch_time = str(time.time())
    gmaps_key = os.environ["GOOGLE_MAPS_API"]
    lat,lon = find_lon_lat()
    local_tz = requests.get("https://maps.googleapis.com/maps/api/timezone/json?location=%s,%s&timestamp=%s&key=%s" % (lat,lon,epoch_time,gmaps_key)).json()
    return local_tz,epoch_time

def rand_pic(len_object):
    return random.randint(1,len_object+1)

def quotes():
    """ an api for computer science quotes """
    quote = requests.get("http://quotes.stormconsultancy.co.uk/quotes.json", headers=headers).json()
    print len(quote), "len_object"
    print rand_pic(len(quote)),"chosen quote by index"
    return quote[rand_pic(len(quote))]

@cache.cached(timeout=60*5, key_prefix="profile")
def profiles():
    """ grabs my github profile api"""
    return requests.get("https://api.github.com/users/jreiher2003", headers=headers).json()
profile = profiles()

def find_current_weather(params):
    """ Open weather map api.  change params for different search"""
    APIKEY = "APPID="+BaseConfig.OPEN_WEATHER_MAP
    URL = "http://api.openweathermap.org/data/2.5/"
    cur = params
    m = URL + cur + APIKEY
    print m
    return requests.get(m, headers=headers).json()

def find_user_weather():
    lat,lon = find_lon_lat()
    return find_current_weather("weather?lat=%s&lon=%s&units=imperial&" % (lat,lon))
# http://api.openweathermap.org/data/2.5/forecast?lat=26.9554&lon=-82.2987&mode=json&units=imperial&appid=d0ee3e692048455da290c0738b4ea751
# http://api.openweathermap.org/data/2.5/forcast?lat=26.9554&lon=-82.2987&mode=json&units=imperial&APPID=d0ee3e692048455da290c0738b4ea751
def find_user_5_day_forcast():
    lat,lon = find_lon_lat() 
    return find_current_weather("forecast/?lat=%s&lon=%s&mode=json&units=imperial&" % (lat,lon))

def find_browers_os_info():
    user_agent = request.headers["User-Agent"]
    return parse(user_agent)

def find_user_sunset_sunrise():
    """finds local user sunrise,sunset, and current local time and names timezone and timezone string"""
    tz, epoch_time = find_local_tz()
    local_name_tz = tz['timeZoneId']
    local_tz_str = str(tz['timeZoneId'])
    weather = find_user_weather()
    s = weather['sys']['sunset']
    r = weather['sys']['sunrise']
    try: 
        wind_degree = weather["wind"]["deg"]
    except KeyError:
        wind_degree = 0
    ss = datetime.fromtimestamp(s).replace(tzinfo=pytz.utc)
    rr = datetime.fromtimestamp(r).replace(tzinfo=pytz.utc)
    ct = datetime.fromtimestamp(float(epoch_time)).replace(tzinfo=pytz.utc)# should already b in utc
    sunset = ss.astimezone(pytz.timezone(local_tz_str))
    sunrise = rr.astimezone(pytz.timezone(local_tz_str))
    current_local_time = ct.astimezone(pytz.timezone(local_tz_str))
    return sunrise,sunset, current_local_time, local_name_tz, local_tz_str, wind_degree


@app.route('/')
def hello_world():
    user_agent = find_browers_os_info()
    user_loc = find_my_loc()
    user_weather = find_user_weather()
    user_5day_forcast = find_user_5_day_forcast()
    sunrise,sunset,current_local_time, local_name_tz, local_tz_str, wind_degree = find_user_sunset_sunrise() 
    wind_direction = degrees_to_cardinal(wind_degree)
    dt = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone(local_tz_str))
    quote = quotes()
    return render_template(
        "index.html",
        dt = dt, 
        profile=profile, 
        quote=quote,
        sunrise=sunrise,
        sunset=sunset,
        user_loc=user_loc,
        user_weather=user_weather,
        user_5day_forcast = user_5day_forcast,
        user_agent=user_agent,
        current_local_time=current_local_time,
        local_name_tz=local_name_tz,
        wind_direction=wind_direction
        )

@app.route("/projects")
@cache.cached(timeout=60*5, key_prefix="projects")
def projects():
    quote = quotes()
    peer = requests.get("https://api.github.com/repos/jreiher2003/peer_flask", headers=headers).json()
    puppy = requests.get("https://api.github.com/repos/jreiher2003/Puppy-Adoption", headers=headers).json()
    portfolio = requests.get("https://api.github.com/repos/jreiher2003/Jeff-Portfolio", headers=headers).json()
    wiki = requests.get("https://api.github.com/repos/jreiher2003/Wiki", headers=headers).json()
    composite = requests.get("https://api.github.com/repos/jreiher2003/Composite", headers=headers).json()
    return render_template(
        "projects.html",
        peer=peer,
        puppy=puppy,
        portfolio=portfolio,
        wiki=wiki,
        composite=composite,
        quote = quote
        )

@app.route("/resume")
def show_resume():
    return render_template(
        "resume.html"
        )



