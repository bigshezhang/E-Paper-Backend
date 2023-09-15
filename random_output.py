import sqlite3
import random
from apscheduler.schedulers.background import BackgroundScheduler
from PIL import Image

from unit import Unit
from converter import image_driver

class RandomOutput:
    photos_name = []
    random_output_scheduler = BackgroundScheduler()

        
    def update_photo_album(self):
        print("更新图片资料中")
        conn = sqlite3.connect(Unit.db_filename)
        cursor = conn.cursor()

        # 查询所有文件名
        cursor.execute('SELECT filename FROM images')
        self.photos_name = [row[0] for row in cursor.fetchall()]

        # 关闭数据库连接
        conn.close()
        
    def default(self):
        self.update_photo_album()
        if self.photos_name:
            random_filename = random.choice(self.photos_name)
            print("Random Filename:", random_filename)
            image = Image.open(Unit.UPLOAD_FOLDER + '/' + random_filename)
            Unit.update_time(Unit)
            Unit.data = image_driver(image)
            

    def __init__(self):
        self.random_output_scheduler.add_job(self.default, 'interval', seconds = 60)
        self.random_output_scheduler.start()
        print("定时器已启动")
        
        