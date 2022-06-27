from models.configs.BaseConfig import BaseConfig

class AnnConfig(BaseConfig):
    def __init__(self,
                 model_file: str = None,
                 one_hot_model_file: str = None,
                 epochs: int = None,
                 batch_size: int = None,
                 test_size: float = None,
                 validation_split: float = None,
                 minimum_accuracy: float = None,
                 ):
        self.model_file = model_file
        self.one_hot_model_file = one_hot_model_file
        self.epochs =  epochs
        self.batch_size =  batch_size
        self.test_size = test_size
        self.validation_split = validation_split
        self.minimum_accuracy = minimum_accuracy

    def is_valid(self):
        pass

