from modules.ui.utils.base_controller import BaseController

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

        self._connectStateUi(self.dynamic_state_ui_connections, SampleModel.instance(), signal=None, idx=self.idx)

        callback = self.__updateSample()
        QtW.QApplication.instance().samplesChanged.connect(callback)
        callback()

        # TODO: TrainConfig.samples is always NONE -> Samples are serialized elsewhere!

    def connectUIBehavior(self):
        self.ui.openWindowBtn.clicked.connect(lambda: self.__openSampleWindow())

    def __updateSample(self):
        def f():
            self._writeControl(self.ui.enabledCbx, "{}.enabled".format(self.idx), SampleModel.instance())
            self._writeControl(self.ui.widthSbx, "{}.width".format(self.idx), SampleModel.instance())
            self._writeControl(self.ui.heightSbx, "{}.height".format(self.idx), SampleModel.instance())
            self._writeControl(self.ui.seedSbx, "{}.seed".format(self.idx), SampleModel.instance())
            self._writeControl(self.ui.promptLed, "{}.prompt".format(self.idx), SampleModel.instance())

        return f

    def __openSampleWindow(self):
        self.openWindow(self.sample_window, fixed_size=True)
        QtW.QApplication.instance().openSample.emit(self.idx)