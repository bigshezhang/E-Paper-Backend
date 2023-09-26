from flask import make_response
from flask_restful import Resource
import sys
from common.unit import Unit
class Display(Resource):
    def get(self):
        byte_stream = Unit.data
        
        response = make_response(byte_stream)
        response.headers["Content-Type"] = "application/octet-stream"
        print({sys.getsizeof(byte_stream)})
        return response
    
class UpdateTime(Resource):
    def get(self):
        response_data = {
            'time': Unit.last_update_time
        }
        return response_data