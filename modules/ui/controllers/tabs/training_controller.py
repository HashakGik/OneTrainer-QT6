from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.ui.controllers.windows.optimizer_controller import OptimizerController

from modules.ui.utils.ModelFlags import ModelFlags


class TrainingController(BaseController):
    state_ui_connections = {
        "": "",
    }


    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/training.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "Training"), parent=parent)

        # TODO: dynamically fill modelSpecificGbx
        # TODO: in UI define valid ranges.
        # TODO: perhaps replace learning rate with lineEdit validated for scientific notation?

        self.optimizer_window = OptimizerController(loader, state=state, mutex=mutex, parent=self)

        pass

    def connectInputValidation(self):
        pass # TODO: resolutionLed validation, learningRateLed validation, minNoisingStrengthSbx <= maxNoisingStrengthSbx

    def connectUIBehavior(self):
        self.ui.optimizerBtn.clicked.connect(lambda: self.openWindow(self.optimizer_window, fixed_size=True))

        # TODO: schedulerCmb enable tableWidget and schedulerClassLed if "CUSTOM" is selected.
        # tableWidget should allow to insert new rows if <Enter> is pressed on a non empty last row
        pass