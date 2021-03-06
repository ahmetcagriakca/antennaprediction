from models.configs.BaseConfig import BaseConfig

class ApiConfig(BaseConfig):

    def __init__(self,
                 environment: str = None,
                 name: str = None,
                 is_debug: bool = None,
                 port: int = None,
                 root_directory: str = None,
                 secret_key: str = None,
                 origins: str = None,
                 authority: str = None,
                 audience: str = None,
                 scopes: [] = None
                 ):
        self.secret_key = secret_key
        self.root_directory: str = root_directory
        self.port: int = port
        self.is_debug: bool = is_debug
        self.name: str = name
        self.environment: str = environment
        self.origins: str = origins
        self.authority: str = authority
        self.audience: str = audience
        self.scopes: [] = scopes

    def is_valid(self):
        pass
