from flask import make_response
from flask_restful import Resource
import sys
from unit import Unit
class Display(Resource):
    def get(self):
        # 创建一个字节流（byte stream），这里示例为一个包含字母的二进制字符串
        byte_stream = Unit.data
        
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