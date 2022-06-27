from infrastructor.api.BaseResponse import BaseResponse
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from infrastructor.api.ErrorHandler import ErrorHandler
from infrastructor.IocManager import IocManager
from infrastructor.exception.OperationalException import OperationalException
from models.configs.ApiConfig import ApiConfig



class FlaskAppWrapper:
    def __init__(self,
                 api_config: ApiConfig):
        self.api_config = api_config
        self.handlers = IocManager.binder.injector.get(ErrorHandler)
        # Application create operations
        self.create_application()

    # Application flask configurations and api endpoint registration
    def create_application(self):
        white_origin = None
        if self.api_config.origins!=None :
            white_origin = self.api_config.origins.split(',')
        CORS(IocManager.app, resources={r"/api/*": {"origins": white_origin}})
        
        # IocManager.app.response_class = BaseResponse
        self.register_error_handlers()

    def register_error_handlers(self):
        IocManager.app.register_error_handler(OperationalException, self.handlers.handle_operational_exception)
        IocManager.app.register_error_handler(Exception, self.handlers.handle_exception)
        IocManager.app.register_error_handler(HTTPException, self.handlers.handle_http_exception)

    def run(self):
        IocManager.app.run(debug=self.api_config.is_debug, host='0.0.0.0', port=self.api_config.port, threaded=False)
