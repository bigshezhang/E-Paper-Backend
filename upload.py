from flask import Flask, request, render_template
import os

app = Flask(__name__)

# 设置上传文件保存的目录
def configure_upload(app):
    # 添加一个路由来处理文件上传
    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # 检查是否有文件被上传
            if 'file' not in request.files:
                return 'No file part'
            
            file = request.files['file']

            # 如果用户未选择文件，浏览器会发送一个空文件
            if file.filename == '':
                return 'No selected file'

            # 如果文件存在，保存它
            if file:
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                return 'File uploaded successfully'

        return render_template('upload.html')
