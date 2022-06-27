
def start():
    from infrastructor.IocManager import IocManager

    import os
    root_directory = os.path.dirname(os.path.abspath(__file__))
    from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper

    IocManager.configure_startup(root_directory=root_directory, app_wrapper=FlaskAppWrapper)
    IocManager.run()


if __name__ == "__main__":
    start()

# application = IocContainer.applicationWrapper()

# if __name__ == "__main__":
#     application.run()

# neural_network_service = IocContainer.neural_network_service()

# if __name__ == "__main__":
#     neural_network_service.run_training_operation()
