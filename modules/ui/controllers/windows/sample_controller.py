from modules.ui.utils.base_controller import BaseController
from modules.ui.controllers.widgets.sample_params import SampleParamsController


from PySide6.QtCore import QCoreApplication as QCA


class SampleController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/sample.ui", state=state, mutex=mutex, name=None, parent=parent)

        self.samplingParams = SampleParamsController(loader, state=state, mutex=mutex, parent=parent)
        self.ui.paramsLay.addWidget(self.samplingParams.ui)

        # TODO: Unlike tab controllers, which are read-write on the state, this window is READ-ONLY!


