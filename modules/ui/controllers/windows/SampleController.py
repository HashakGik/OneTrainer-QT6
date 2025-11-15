from modules.ui.controllers.BaseController import BaseController
from modules.ui.controllers.widgets.SampleParamsController import SampleParamsController


class SampleController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/sample.ui", name=None, parent=parent)

        self.samplingParams = SampleParamsController(loader, parent=parent)
        self.ui.paramsLay.addWidget(self.samplingParams.ui)

        # TODO: Unlike tab controllers, which are read-write on the state, this window is READ-ONLY!


