from datetime import datetime
from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse



class Unit:
    app = Flask(__name__)
    api = Api(app)
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.template_folder = 'templates'
    
    site_path = 'http://127.0.0.1:5001/'
    data = bytes([0x00] * 192000)
    # data = [0x00] * 192000
    last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def update_time(self):
        self.last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
