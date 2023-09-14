from flask import Flask, Response, make_response
from flask_restful import Resource
from datetime import datetime
import sys
from unit import Unit
import c7_image
class Display(Resource):
    def get(self):
        # 创建一个字节流（byte stream），这里示例为一个包含字母的二进制字符串
        byte_stream = c7_image.Image7color
        
        response = make_response(byte_stream)
        response.headers["Content-Type"] = "application/octet-stream"
        print({sys.getsizeof(byte_stream)})
        # 返回响应对象
        return response
    
class UpdateTime(Resource):
    def get(self):
        response_data = {
            'time': Unit.last_update_time
        }

        return response_data