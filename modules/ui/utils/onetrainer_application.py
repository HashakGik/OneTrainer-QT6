from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Signal

from modules.util.enum.ModelType import ModelType
from modules.util.enum.TrainingMethod import TrainingMethod

class OnetrainerApplication(QApplication):
    stateChanged = Signal() # Signal for global UI invalidation (e.g., when a config file is reloaded from disk).
    modelChanged = Signal(ModelType, TrainingMethod) # Signal for changed model/training method. Emit with emit(newmodel, newmethod) so that receivers can use directly those messages.

    # optimizerChanged, and then what else? Remember that tool windows actually read the state directly, without updating UI elements, they do not need a signal
