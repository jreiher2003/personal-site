import os
import datetime
from flask import Flask 
from flask_caching import Cache

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS'])
cache = Cache(app)

from app import views

@app.template_filter()
def date_s(value):
    """convert a datetime object to a formated string """
    return value.strftime("%A, %d %b %Y %I:%M %p")

@app.template_filter()
def just_time(value):
    """convert a datetime object to a formated string """
    return value.strftime("%I:%M %p")

@app.template_filter()
def time_stamp(value):
    """ convert epoch time to strftime """
    return datetime.datetime.fromtimestamp(value).strftime("%c")

app.jinja_env.filters["date_s"] = date_s
app.jinja_env.filters["just_time"] = just_time
app.jinja_env.filters["time_stamp"] = time_stamp
