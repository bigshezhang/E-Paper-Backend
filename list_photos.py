import os
from flask_restful import Resource, Api, reqparse
from flask import Flask, send_from_directory

from unit import Unit

def show_uploads(app):
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

class ListUploadedPhotos(Resource):
    def get(self):
        photo_list = []
        upload_folder = 'uploads'
        for filename in os.listdir(upload_folder):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                photo_url = os.path.join(upload_folder, filename)
                photo_list.append(Unit.site_path + photo_url)
        return {'photos': photo_list}

