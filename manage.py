import os 

from app import app 
import logging

from flask_script import Manager, Server 
 
app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=5015))

if __name__ == '__main__':
    manager.run()