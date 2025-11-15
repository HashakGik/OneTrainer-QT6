from modules.ui.controllers.BaseController import BaseController

from modules.ui.models.SampleModel import SampleModel

import PySide6.QtWidgets as QtW

class SampleController(BaseController):
    def __init__(self, loader, sample_window, idx, parent=None):
        self.idx = idx
        self.sample_window = sample_window

        super().__init__(loader, "modules/ui/views/widgets/sample.ui", name=None, parent=parent)

        self.dynamic_state_ui_connections = {
            "{idx}.enabled": "enabledCbx",
            "{idx}.width": "widthSbx",
            "{idx}.height": "heightSbx",
            "{idx}.seed": "seedSbx",
            "{idx}.prompt": "promptLed",
        }

        self._connectStateUi(self.dynamic_state_ui_connections, SampleModel.instance(), signal=QtW.QApplication.instance().samplesChanged, update_after_connect=True, idx=self.idx)

    def _connectUIBehavior(self):
        self.connect(self.ui.openWindowBtn.clicked, lambda: self.__openSampleWindow())


    def __openSampleWindow(self):
        self.openWindow(self.sample_window, fixed_size=True)
        QtW.QApplication.instance().openSample.emit(self.idx)