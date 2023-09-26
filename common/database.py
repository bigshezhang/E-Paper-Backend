import os
from flask_restful import Resource, reqparse
from datetime import datetime
import sqlite3

from common.unit import Unit

class Photo:
    id: int
    file_name: str
    upload_time: str
    description: str
    url: str

    def __init__(self, id, file_name, upload_time, description):
        self.id = id
        self.file_name = file_name
        self.upload_time = upload_time
        self.description = description
        self.url = Unit.site_path + 'uploads/' + file_name

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
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM images WHERE filename = ?', (filename,))
        photo = cursor.fetchone()
        if photo == None:
            upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO images (filename, upload_time, description)
                VALUES (?, ?, ?)
            ''', (filename, upload_time, ''))
            conn.commit()
        else:
            raise Exception("Already had the same photo")
        conn.close()
        
    def get_photo_by_filename(self, filename):
        conn = sqlite3.connect(Unit.db_filename)
        cursor = conn.cursor()
        # 执行查询
        cursor.execute(
            'SELECT * FROM images WHERE filename = ?', (filename,))

        # 获取查询结果
        photo = cursor.fetchone()

        if photo == None:
            raise Exception("No such file")

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
        
    def list_photos(self):
        photo_list = [Photo]
        photo_list.clear()
        conn = sqlite3.connect(Unit.db_filename)
        cursor = conn.cursor()
        # 查询所有文件名
        try:
            # 执行数据库查询
            cursor.execute(
                'SELECT id, filename, upload_time, description FROM images')
            for row in cursor:
                photo_list.append(
                    Photo(
                        row[0], row[1], row[2], row[3],
                    )
                )
            conn.close()
            return [{
                    "id": photo.id,
                    "file_name": photo.file_name,
                    "upload_time": photo.upload_time,
                    "description": photo.description,
                    "url": photo.url
                    }for photo in photo_list]
        except sqlite3.Error as e:
            print("SQLite error:", e)

        # 关闭数据库连接
        conn.close()

    def get_photo_description(self, filename):
        return self.get_photo_by_filename(self, filename)['description']

    def update_photo_description(self, filename, new_description):
        conn = sqlite3.connect(Unit.db_filename) 
        cursor = conn.cursor()

        # 执行更新操作
        cursor.execute(
            'UPDATE images SET description = ? WHERE filename = ?', (new_description, filename))

        # 提交事务
        conn.commit()
        conn.close()
        
    def delete_photo(self, filename):
        # 删除本地存储的照片文件
        photo_path = os.path.join(
            Unit.UPLOAD_FOLDER, str(filename)) 
        try:
            os.remove(photo_path)
        except Exception as e:
            raise Exception("Failed to delete file: " + str(e))

        conn = sqlite3.connect(Unit.db_filename) 
        cursor = conn.cursor()

        try:
            # 删除数据库记录
            cursor.execute(
                'DELETE FROM images WHERE filename = ?', (filename,))
            # 提交事务
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception("Failed to delete database record: " + str(e))
        finally:
            conn.close()
