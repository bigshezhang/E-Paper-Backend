from flask import Flask, render_template
from upload import configure_upload  # 导入upload模块

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.template_folder = 'templates'

# 配置文件上传
configure_upload(app)

if __name__ == '__main__':
    app.run()
