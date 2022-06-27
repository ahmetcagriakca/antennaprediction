from datetime import datetime
from models.configs.ApiConfig import ApiConfig

from flask_restplus import fields

from infrastructor.IocManager import IocManager
from infrastructor.exception.OperationalException import OperationalException
from flask import request

# @IocManager.app.before_request
# def before_request(response):
#     api_config:ApiConfig = IocManager.config_manager.get(ApiConfig)
#     white_origin=None
#     if api_config.origins!=None :
#         white_origin= api_config.origins.split(',')
#     if (white_origin!= None and len(white_origin)==1 and white_origin[0]=='*') or \
#         ('Origin' in request.headers and request.headers['Origin'] in white_origin)  :
#         response.headers['Access-Control-Allow-Origin'] = request.headers['Origin'] 
#         # response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
#         # response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        
#     response.headers['Server'] = ''
#     return response

@IocManager.app.after_request
def after_request(response):
    api_config:ApiConfig = IocManager.config_manager.get(ApiConfig)
    white_origin=None
    if api_config.origins!=None :
        white_origin= api_config.origins.split(',')
    if (white_origin!= None and len(white_origin)==1 and white_origin[0]=='*') or \
        ('Origin' in request.headers and request.headers['Origin'] in white_origin)  :
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin'] 
        # response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        # response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Server'] = ''
    return response

@IocManager.api.errorhandler(OperationalException)
def handle_error(error):
    return CommonModels.get_error_response(message=error)

@IocManager.api.errorhandler(Exception)
def handle_error(error):
    return CommonModels.get_error_response(message=error)

class CommonModels:
    SuccessModel = IocManager.api.model('SuccessModel', {
        'IsSuccess': fields.Boolean(description='Service finished operation with successfully', default=True),
        'Message': fields.String(description='Service result values', default="Operation Completed"),
        'Result': fields.Raw(description='Service result values'),
    })

    def date_converter(o):
        if isinstance(o, datetime):
            return o.__str__()
    @staticmethod
    def get_response(result=None, message=None):
        return {'Result': result,'Message': message}

    @staticmethod
    def get_error_response(message):
        return {"IsSuccess": False, 'Message': message}


class EntityModel:
    def __init__(self,
                 Id: int = None,
                 ):
        self.Id: int = Id
