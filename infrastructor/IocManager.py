from infrastructor.api.FlaskBase import FlaskBase
from infrastructor.auth.OAuthFilter import OAuthFilter
import sys
from flask_injector import request, FlaskInjector
from flask_restplus import Api
from injector import singleton, Injector, threadlocal, Binder
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.dependency.scopes import ISingleton, IScoped
from infrastructor.utils.ConfigManager import ConfigManager
from infrastructor.utils.Utils import Utils
from models.configs.ApiConfig import ApiConfig
from models.configs.AnnConfig import AnnConfig
from models.configs.FeatureConfig import FeatureConfig
from models.configs.LogConfig import LogConfig
from models.configs.OtherConfig import OtherConfig


class IocManager:
    app: FlaskBase = None
    api: Api = None
    binder: Binder = None
    app_wrapper = None
    config_manager = None
    injector: Injector = None
    oauth = None

    # wrapper required for dependency
    @staticmethod
    def configure_startup(root_directory, app_wrapper=None):
        IocManager.config_manager = ConfigManager(root_directory)
        # ApiConfig getting with type
        IocManager.app_wrapper = app_wrapper
        # Configuration initialize
        IocManager.config_manager = IocManager.config_manager
        # ApiConfig gettin with type
        api_config = IocManager.config_manager.get(ApiConfig)
        IocManager.oauth = OAuthFilter(api_config=api_config)

        # Flask instantiate
        IocManager.app = FlaskBase(api_config.name)
        IocManager.api = Api(app=IocManager.app)

        # Importing all modules for dependency
        sys.path.append(api_config.root_directory)
        folders = Utils.find_sub_folders(api_config.root_directory)
        module_list, module_attr_list = Utils.get_modules(folders)
        IocManager.injector = Injector()
        # Flask injector configuration
        FlaskInjector(app=IocManager.app, modules=[IocManager.configure], injector=IocManager.injector)

    @staticmethod
    def run():
        IocManager.injector.get(IocManager.app_wrapper).run()

    def configure(binder: Binder):
        IocManager.binder = binder

        for config in IocManager.config_manager.get_all():
            if config.get("type") is not None:
                binder.bind(
                    config.get("type"),
                    to=config.get("instance"),
                    scope=singleton,
                )

        for singletonScope in ISingleton.__subclasses__():
            binder.bind(
                singletonScope,
                to=singletonScope,
                scope=singleton,
            )

        for scoped in IScoped.__subclasses__():
            binder.bind(
                scoped,
                to=scoped,
                scope=threadlocal,
            )

        for controller in ResourceBase.__subclasses__():
            binder.bind(
                controller,
                to=controller,
                scope=request,
            )
        if IocManager.app_wrapper is not None:
            api_config = IocManager.config_manager.get(ApiConfig)
            binder.bind(
                IocManager.app_wrapper,
                to=IocManager.app_wrapper(api_config)
            )
