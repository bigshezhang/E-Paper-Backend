import os
from flask_restful import Resource, reqparse
from datetime import datetime
import sqlite3

from common.unit import Unit
from common.database import Photo, Database

class PhotoApi:
    class GetPhotoByFilename(Resource):
        def get(self, filename):
            try:
                return {"success": True, "data": Database.get_photo_by_filename(filename)}
            except Exception as e:
                print(e)
                return {"success": False, "error": str(e)}

    class ListPhotos(Resource):
        photo_list = []
        def get(self):
            try:
                Database.list_photos(Database)
                return Database.list_photos(Database)
            except sqlite3.Error as e:
                return {
                    "success": False
                }

    class UpdatePhotoDescription(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('description', type=str,
                                location='form')  # 描述参数
            parser.add_argument('filename', type=str, location='form')
            args = parser.parse_args()
            try:
                Database.update_photo_description(
                    args['filename'], args['description'])
                return {"success": True}
            except Exception as e:
                print(e)
                return {"success": False, "error": str(e)}

    class DeletePhoto(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('filename', type=str, location='form')
            args = parser.parse_args()
            try:
                Database.delete_photo(args['filename'])
                return {"success": True}
            except Exception as e:
                return {"success": False, "error": str(e)}


