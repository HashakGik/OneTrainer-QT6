from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Signal

from modules.util.enum.ModelType import ModelType
from modules.util.enum.TrainingMethod import TrainingMethod
from modules.util.enum.Optimizer import Optimizer

class OnetrainerApplication(QApplication):
    # Signal for global UI invalidation (e.g., when a config file is reloaded from disk).
    stateChanged = Signal()

    # Signals for dynamic widget lists and sub windows. The passed value is the currently selected element.
    conceptsChanged = Signal()
    singleConceptChanged = Signal(int)

    samplesChanged = Signal()
    openSample = Signal(int)

    embeddingsChanged = Signal()

    # Signals used to update only a subset of elements, passing relevant data for redrawing.
    modelChanged = Signal(ModelType, TrainingMethod) # Signal for changed model/training method. Emit with emit(newmodel, newmethod) so that receivers can use directly those messages.
    optimizerChanged = Signal(Optimizer)

    #def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)

        #self.stateChanged.connect(self.embeddingsChanged)
        #self.stateChanged.connect(self.conceptsChanged)
        #self.stateChanged.connect(self.samplesChanged)