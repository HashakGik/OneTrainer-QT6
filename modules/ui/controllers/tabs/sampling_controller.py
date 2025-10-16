from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController

from modules.ui.controllers.widgets.sample_controller import SampleController

class SamplingController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/sampling.ui", state=state, name=QCA.translate("main_window_tabs", "Sampling"), parent=parent)
        self.children = {}
        pass

    def connectUIBehavior(self):
        self.ui.addSampleBtn.clicked.connect(lambda: self.__appendSample())

    def __appendSample(self):
        wdg = SampleController(self.loader, len(self.children), state=self.state, parent=self)
        self.children[len(self.children)] = wdg
        self._appendWidget(self.ui.listWidget, wdg, self_delete_btn=True, self_clone_btn=True)