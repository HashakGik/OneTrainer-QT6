import sys
from modules.ui.controllers.onetrainer import OnetrainerController

from modules.ui.utils.onetrainer_application import OnetrainerApplication
from PySide6.QtUiTools import QUiLoader

from PySide6.QtCore import QBasicMutex

from modules.ui.utils.sn_led import SNLineEdit

from modules.util.config.TrainConfig import TrainConfig
from modules.util.config.CloudConfig import CloudConfig
from modules.util.config.ConceptConfig import ConceptConfig
from modules.util.config.SecretsConfig import SecretsConfig
from modules.util.config.SampleConfig import SampleConfig

from PySide6.QtCore import Qt

if __name__ == "__main__":
    app = OnetrainerApplication(sys.argv)
    loader = QUiLoader()
    loader.registerCustomWidget(SNLineEdit) # TODO: REMEMBER TO PROMOTE IN UI FILES! And to manually set min and max of controls (if present).

    state = TrainConfig.default_values() # .to_dict() # TODO: Maybe this should become singleton?
    mutex = QBasicMutex()


    # {
    #     "train": TrainConfig.default_values(), # MAYBE TRAIN AND LOCK ARE ENOUGH -> self.state, self.mutex
    #     "secrets": SecretsConfig.default_values(),
    #     "cloud": CloudConfig.default_values(),
    #     "concepts": ConceptConfig.default_values(),
    #     "sample": SampleConfig.default_values(),
    #     # TODO: also needs an invalidate mechanism. Observer pattern on a boolean set to True at the beginning and every time a config is loaded?
    # } # TODO: is this enough to capture every state?
    # TODO: load last values with a QSetting? (last used (save or load) filename: if exists load, else load default)
    # IDEA: abstractController exposes self.connections as a dict ui_element -> model_element. the constructor of each subclass populates that model.
    #       AbstractController then implements lock -> read/write -> unlock as slot and connects every element with a for loop (Either define self connections as properties, or invoke connection at the end of each constructor, otherwise the list would be empty)
    # PROBLEM: objects are passed by reference, but atoms are passed by value. The setter mechanism must work in a path-like fashion (eg. "train/cautious_mask", "train/concepts/0/concept/image/enable_random_flip")?
    # IMPORTANT: release lock in finally branch!!!

    # TODO: extract GUI agnostic functions (eg. start training, invalidate state, etc.) in modules.ui.models, grouped by logic family, not by ui element (TrainingModel, samplingModel, etc.)
    # Otherwise, if the implementation remains like the current one, it becomes a Model-View architecture, instead of a Model-View-Controller and decoupling is incomplete.


    onetrainer = OnetrainerController(loader, state=state, mutex=mutex)

    # Invalidate ui elements after the controllers are set up, but before showing them.
    app.stateChanged.emit() # TODO: BUG! Since only QWidget values are connected to this Signal, none of the connections for UI behavior defined in connectUIBehavior() is fired. Each controller should also attach those Slots to invalid
    onetrainer.ui.show()

    sys.exit(app.exec())