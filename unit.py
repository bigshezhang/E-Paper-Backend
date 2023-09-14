from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse



class Unit:
    app = Flask(__name__)
    api = Api(app)
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.template_folder = 'templates'
    
    site_path = 'http://127.0.0.1:5000/'
