from datetime import datetime
from flask import Flask, render_template
from flask_restful import Api
from dotenv import load_dotenv
import os

from mqtt_server import MqttServer
from flask_cors import CORS

class Unit:
    load_dotenv()
    site_path = os.getenv("SITE_PATH")
    
    mqttServer = MqttServer()
    app = Flask(__name__)
    api = Api(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app, resources={r"/uploads/*": {"origins": "*"}})
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.template_folder = 'templates'
    
    data = bytes([0x00] * 192000)
    # data = [0x00] * 192000
    last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db_filename = 'photos.db'
    
    def update_time(self):
        self.last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
unit = Unit()