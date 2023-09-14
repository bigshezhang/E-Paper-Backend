from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from upload import configure_upload, FileUpload  # 导入upload模块
from list_photos import show_uploads, ListUploadedPhotos
# 配置文件上传

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.template_folder = 'templates'
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api.add_resource(FileUpload, '/api/upload')
api.add_resource(ListUploadedPhotos, '/api/photos')

configure_upload(app)
show_uploads(app)

if __name__ == '__main__':
    app.run()
