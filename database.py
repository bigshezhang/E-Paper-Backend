import os
from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Resource , reqparse
from datetime import datetime

import sqlite3

from unit import Unit

class Database:
    def create_table():
        conn = sqlite3.connect(Unit.db_filename)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                upload_time TIMESTAMP NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
        
    def add_photo(filename):
        conn = sqlite3.connect(Unit.db_filename)
        upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO images (filename, upload_time, description)
            VALUES (?, ?, ?)
        ''', (filename, upload_time, ''))
        conn.commit()
        conn.close()
        
    class GetPhotoByFilename(Resource):
        def get(self,filename):
            try:
                
                # print(filename)
                return {"success": True, "data" : self.get_photo_by_filename(filename)}
            except Exception as e:
                print(e)
                return {"success": False, "error": str(e)}
            
        
        def get_photo_by_filename(self, filename):
            conn = sqlite3.connect(Unit.db_filename) 
            cursor = conn.cursor()
            
            # 执行查询
            cursor.execute('SELECT * FROM images WHERE filename = ?', (filename,))
            
            # 获取查询结果
            photo = cursor.fetchone()
            
            if photo == None:
                raise Exception ("No such file")
            
            
            conn.close()
            try:
                # 将查询结果转化为字典
                photo_dict = {
                    'id': photo[0],
                    'filename': photo[1],
                    'upload_time': photo[2],
                    'description': photo[3]
                }

                return photo_dict
            except Exception as e:
                print(e)
                return e
               
        
        
    class UpdatePhotoDescription(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('description', type=str,location='form')  # 描述参数
            parser.add_argument('filename', type=str,location='form')
            args = parser.parse_args()
            try:
                self.update_photo_description(args['filename'], args['description'])
                return {"success": True}
            except Exception as e:
                print(e)
                return {"success": False, "error": str(e)}
        
        
        def update_photo_description(self, filename, new_description):
            conn = sqlite3.connect(Unit.db_filename)  # 请替换成你的数据库文件路径
            cursor = conn.cursor()
            
            # 执行更新操作
            cursor.execute('UPDATE images SET description = ? WHERE filename = ?', (new_description, filename))
            
            # 提交事务
            conn.commit()
            conn.close()
        
        
    class DeletePhoto(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('filename', type=str, location='form')
            args = parser.parse_args()
            try:
                self.delete_photo(args['filename'])
                return {"success": True}
            except Exception as e:
                return {"success": False, "error": str(e)}

        def delete_photo(self, filename):
            # 删除本地存储的照片文件
            photo_path = os.path.join(Unit.UPLOAD_FOLDER, str(filename))  # 替换成你的照片存储路径
            try:
                os.remove(photo_path)
            except Exception as e:
                raise Exception("Failed to delete file: " + str(e))

            conn = sqlite3.connect(Unit.db_filename)  # 替换成你的数据库文件路径
            cursor = conn.cursor()
            
            try:
                # 删除数据库记录
                cursor.execute('DELETE FROM images WHERE filename = ?', (filename,))
                # 提交事务
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise Exception("Failed to delete database record: " + str(e))
            finally:
                conn.close()

        
        
        
        
