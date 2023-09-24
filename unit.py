from datetime import datetime
from flask import Flask, render_template
from flask_restful import Api
from dotenv import load_dotenv
import os

class Unit:
    site_path = ''
    def __init__(self):
        load_dotenv()
        self.site_path = os.getenv("SITE_PATH")
        
    app = Flask(__name__)
    api = Api(app)
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.template_folder = 'templates'
    
    data = bytes([0x00] * 192000)
    # data = [0x00] * 192000
    last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db_filename = 'photos.db'
    
    def update_time(self):
        self.last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
