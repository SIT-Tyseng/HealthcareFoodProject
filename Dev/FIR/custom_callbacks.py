from pytorch_lightning.callbacks import EarlyStopping, Callback

class TrainCallback(Callback):
    def __init__(self):
        super().__init__()

    def on_train_start(self, trainer, pl_module):
        print("Starting to train!")

    def on_train_end(self, trainer, pl_module):
        print("Training is done.")

    def on_validation_start(self, trainer, pl_module):
        print("Starting to validate!")

    def on_validation_end(self, trainer, pl_module):
        print("Validation is done.")

    # def on_test_start(self, trainer, pl_module):
    #     print("Starting to test!")

    # def on_test_end(self, trainer, pl_module):
    #     print("Testing is done.")

class TestCallback(Callback):
    def __init__(self):
        super().__init__()

    def on_test_start(self, trainer, pl_module):
        print("Starting to test!")

    def on_test_end(self, trainer, pl_module):
        print("Testing is done.")
