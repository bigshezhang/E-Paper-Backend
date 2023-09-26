from flask import send_from_directory
from common.database import Database
from network.display import Display, UpdateTime
from network.upload import FileUpload  # 导入upload模块
import threading
import sys
import os
from common.unit import Unit
from network.photo_api import PhotoApi
from common.random_output import RandomOutput
from network.mqtt_server import MqttServer
# 配置文件上传

Unit.working_path = os.getcwd()

mqtt_thread = threading.Thread(target=Unit.mqttServer.mqtt_thread)
mqtt_thread.start()

def show_uploads(app):
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

Database.create_table()
show_uploads(Unit.app)

Unit.api.add_resource(FileUpload, '/api/upload')
Unit.api.add_resource(Display, '/api/display')
Unit.api.add_resource(UpdateTime, '/api/updatetime')
Unit.api.add_resource(PhotoApi.GetPhotoByFilename, '/api/get_photo_by_filename/<string:filename>')
Unit.api.add_resource(PhotoApi.UpdatePhotoDescription, '/api/update_photo_description')
Unit.api.add_resource(PhotoApi.DeletePhoto, '/api/delete_photo')
Unit.api.add_resource(PhotoApi.ListPhotos,'/api/photos')

if __name__ == '__main__':
    RandomOutput()

    Unit.app.run(host='0.0.0.0',port=5001)
    
