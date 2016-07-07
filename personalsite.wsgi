#!/usr/bin/python
import sys
import logging
activate_this = '/var/www/personalsite/personalsite/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/personalsite/")


from app import app 