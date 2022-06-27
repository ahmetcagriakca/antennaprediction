from models.configs.BaseConfig import BaseConfig


class OtherConfig(BaseConfig):
    def __init__(self,
                 model_path: str = None,
                 backup_path: str = None,
                 file_name: str = None,
                 root_directory: str = None,
                 log_path: str = None
                 ):
        self.log_path = log_path
        self.model_path = model_path
        self.backup_path = backup_path
        self.file_name = file_name
        self.root_directory = root_directory

    def is_valid(self):
        pass
