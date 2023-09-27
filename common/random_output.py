import sqlite3
import random
from apscheduler.schedulers.background import BackgroundScheduler
from PIL import Image
from common.database import Database

from common.unit import Unit

from image_process.image_driver import ImageDriver

class RandomOutput:
    photos_name = []
    random_output_scheduler = BackgroundScheduler()
   
    def update_photo_album(self):
        # print("更新图片资料中")
        conn = sqlite3.connect(Unit.db_filename)
        cursor = conn.cursor()

        # 查询所有文件名
        try:
    # 执行数据库查询
            cursor.execute('SELECT filename FROM images')
            self.photos_name = [row[0] for row in cursor.fetchall()]
            # print(self.photos_name)
        except sqlite3.Error as e:
            print("SQLite error:", e)

        # 关闭数据库连接
        conn.close()
        
    def default(self):
        self.update_photo_album()
        # print (self.photos_name)
        if self.photos_name:
            random_filename = random.choice(self.photos_name)
            image = Image.open(Unit.UPLOAD_FOLDER + '/' + random_filename)
            ImageDriver.publish_image(ImageDriver, image, random_filename)
            

    def __init__(self):
        self.default()
        self.random_output_scheduler.add_job(self.default, 'interval', seconds = 1)
        self.random_output_scheduler.start()
        print("定时器已启动")
        
        