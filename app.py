from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from display import Display, UpdateTime
from upload import configure_upload, FileUpload  # 导入upload模块
from list_photos import show_uploads, ListUploadedPhotos
from unit import Unit
# 配置文件上传


configure_upload(Unit.app)
show_uploads(Unit.app)

Unit.api.add_resource(FileUpload, '/api/upload')
Unit.api.add_resource(ListUploadedPhotos, '/api/photos')
Unit.api.add_resource(Display, '/api/display')
Unit.api.add_resource(UpdateTime, '/api/updatetime')

if __name__ == '__main__':
    Unit.app.run(host='0.0.0.0',port=5001)
