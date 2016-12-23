import random
import requests
from app import app
from flask import render_template, url_for, redirect
from config import BaseConfig 

def header():
    return {"Content-Type": "application/json", "User-Agent": "jreiher2003"}
headers = header()

def rand_pic(len_object):
    return random.randint(1,len_object+1)

def quotes():
    quote = requests.get("http://quotes.stormconsultancy.co.uk/quotes.json", headers=headers).json()
    return quote[rand_pic(len(quote))]


def profiles():
    return requests.get("https://api.github.com/users/jreiher2003", headers=headers).json()
profile = profiles()

APIKEY = "APPID="+BaseConfig.OPEN_WEATHER_MAP
URL = "http://api.openweathermap.org/data/2.5/"
def find_current_weather():
    cur = "weather?zip=34224,us&units=imperial&"
    m = URL + cur + APIKEY
    return requests.get(m, headers=headers).json()
weather = find_current_weather()

@app.route('/')
def hello_world():
    quote = quotes()
    print find_current_weather()
    return render_template(
        "index.html", 
        profile=profile, 
        quote=quote,
        weather=weather)

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



