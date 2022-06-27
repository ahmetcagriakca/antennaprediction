


def start():
    from infrastructor.IocManager import IocManager

    import os
    root_directory = os.path.dirname(os.path.abspath(__file__))
    from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper

    IocManager.configure_startup(root_directory=root_directory, app_wrapper=FlaskAppWrapper)
    # IocManager.run()


if __name__ == "__main__":
    start()
    from domain.ai.services.NeuralNetworkService import NeuralNetworkService
    from infrastructor.IocManager import IocManager
    service = IocManager.injector.get(NeuralNetworkService)
    service.run_training_operation()
    print("training finished")