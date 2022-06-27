from models.configs.BaseConfig import BaseConfig

class FeatureConfig(BaseConfig):
    def __init__(self,
                 input_format: str = None,
                 output_format: str = None,
                 ):
        self.input_format = input_format
        self.output_format = output_format

    def is_valid(self):
        pass
