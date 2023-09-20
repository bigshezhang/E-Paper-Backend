from flask import send_from_directory
from display import Display, UpdateTime
from upload import configure_upload, FileUpload  # 导入upload模块

from unit import Unit
from database import Database
from random_output import RandomOutput
# 配置文件上传

def show_uploads(app):
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

Database.create_table()
configure_upload(Unit.app)
show_uploads(Unit.app)

Unit.api.add_resource(FileUpload, '/api/upload')
Unit.api.add_resource(Display, '/api/display')
Unit.api.add_resource(UpdateTime, '/api/updatetime')
Unit.api.add_resource(Database.GetPhotoByFilename, '/api/get_photo_by_filename/<string:filename>')
Unit.api.add_resource(Database.UpdatePhotoDescription, '/api/update_photo_description')
Unit.api.add_resource(Database.DeletePhoto, '/api/delete_photo')
Unit.api.add_resource(Database.ListPhotos,'/api/photos')

if __name__ == '__main__':
    RandomOutput()

    Unit.app.run(host='0.0.0.0',port=5001)
    
