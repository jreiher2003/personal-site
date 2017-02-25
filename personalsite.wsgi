#!/usr/bin/python
import os
import sys
import logging
activate_this = '/var/www/personalsite/personalsite/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/personalsite/personalsite/")

os.environ['APP_SETTINGS'] = 'config.ProductionConfig'
os.environ['SECRET_KEY'] = '\x86)U\xe5\xf8\xed\x99\xc6M\xb7?\xda<R\xcd\xd2\x8f\xab\x9e\xcc0\x8e\xa1'
os.environ["OPEN_WEATHER_MAP"] = "d0ee3e692048455da290c0738b4ea751"
os.environ["GOOGLE_MAPS_API"] = "AIzaSyAPoTbuKvHLe7vwxZ4xPjj9GWGW_XInX8A"


from app import app as application



