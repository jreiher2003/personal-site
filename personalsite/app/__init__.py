import os
from flask import Flask 

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS'])

from app import views

@app.template_filter()
def date_s(value):
    """convert a datetime object to a formated string """
    return value.strftime("%A, %d %b %Y %I:%M %p")

app.jinja_env.filters["date_s"] = date_s
