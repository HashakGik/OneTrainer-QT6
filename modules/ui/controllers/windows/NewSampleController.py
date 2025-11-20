from modules.ui.controllers.BaseController import BaseController
from modules.ui.controllers.widgets.SampleParamsController import SampleParamsController


from modules.ui.models.SampleModel import SampleModel

import PySide6.QtWidgets as QtW


class NewSampleController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/new_sample.ui", name=None, parent=parent)

    def _setup(self):
        self.samplingParams = SampleParamsController(self.loader, model_instance=SampleModel.instance(), use_idx=True, update_signal=QtW.QApplication.instance().openSample, parent=self.parent)
        self.ui.paramsLay.addWidget(self.samplingParams.ui)

    def _connectUIBehavior(self):
        self.connect(self.ui.okBtn.clicked, self.__saveSample())

    def __saveSample(self):
        def f():
            QtW.QApplication.instance().samplesChanged.emit()
            self.ui.hide()

        return f