from app import app
from flask import render_template, url_for, redirect
import random 
import requests


a = {"I want to put a ding in the universe.": "Steve Jobs", "As we express our gratitude, we must never forget that the highest appreciation is not to utter words, but to live by them.": "John F. Kennedy", "I know where I'm going and I know the truth, and I don't have to be what you want me to be. I'm free to be what I want.": "Muhammand Ali", "Age is whatever you think it is. You are as old as you think you are.": "Muhammand Ali", "Always be yourself, express yourself, have faith in yourself, do not go out and look for a successful personality and duplicate it.": "Bruce Lee", "The starting point of all achievement is desire.": "Napoleon Hill", "Success consists of going from failure to failure without loss of enthusiasm.": "Winston Churchill"}

@app.route('/')
def hello_world():
    QUOTE = random.choice(list(a.items()))
    return render_template("index.html", QUOTE=QUOTE)

@app.route("/projects")
def projects():
    QUOTE = random.choice(list(a.items()))
    headers = {"Content-Type": "application/json", "User-Agent": "jreiher2003"}
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
        QUOTE=QUOTE
        )

@app.route("/resume")
def show_resume():
    return render_template("JeffreyReiherResume.html")


