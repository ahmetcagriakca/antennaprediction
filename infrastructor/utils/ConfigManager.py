import ctypes
import os
import sys

import yaml
from infrastructor.utils.Utils import Utils
from models.configs.BaseConfig import BaseConfig


class ConfigManager:
    def __init__(self, root_directory: str) -> None:
        # Create an empty list with items of type T
        self.configs = self.__get_configs(root_directory)

    def get_all(self):
        return self.configs

    def get_by_name(self, name):
        for config in self.configs:
            if config["name"] == name:
                return config.get("instance")

    def get(self, generic_type):
        for config in self.configs:
            config_type = config.get("type")
            if config_type is generic_type:
                return config.get("instance")

    def empty(self) -> bool:
        return not self.items

    @staticmethod
    def __get_configs(root_directory) -> []:
        config_path = os.path.join(root_directory, "models", "configs")
        sys.path.append(config_path)
        module_list, module_attr_list = Utils.get_modules([config_path])
        environment = os.getenv('PYTHON_ENVIRONMENT', None)
        config_path = "application.yml"
        if environment is not None:
            config_path_splitted = "application.yml".split('.')
            config_path = f'{config_path_splitted[0]}.{environment}.{config_path_splitted[1]}'
        with open(os.path.join(root_directory, config_path), 'r') as yml_file:
            loaded_configs = yaml.load(yml_file, Loader=yaml.FullLoader)
        configs = []
        for config in BaseConfig.__subclasses__():
            config_instance = config()

            class_name = Utils.replace_last(config_instance.__class__.__name__, 'Config', '')
            if class_name not in loaded_configs:
                class_name = class_name.upper()
            config_properties = [a for a in dir(config_instance) if not (a.startswith('_'))]
            for prop in config_properties:
                prop_name = prop.upper()
                environment_name = f'{class_name}_{prop_name}'
                if class_name in loaded_configs:
                    if prop_name in loaded_configs[class_name]:
                        config_value = loaded_configs[class_name][prop_name]
                    elif prop_name == 'RootDirectory' or prop_name == 'ROOT_DIRECTORY':
                        config_value = root_directory
                    else:
                        config_value = None

                prop_value = os.getenv(environment_name, config_value)
                setattr(config_instance, prop, prop_value)
            configs.append({"name": class_name, "type": config, "instance": config_instance})
        for key in loaded_configs.keys():
            has_key = False
            for conf in configs:
                if conf["name"] == key:
                    has_key = True

            if not has_key:
                configs.append({"name": key, "type": None, "instance": loaded_configs[key]})

        return configs
