from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.ui.controllers.widgets.sample_controller import SampleController
from modules.ui.controllers.windows.new_sample_controller import NewSampleController

from modules.util.enum.TimeUnit import TimeUnit
from modules.util.enum.ImageFormat import ImageFormat

class SamplingController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/sampling.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "Sampling"), parent=parent)
        self.children = {}
        self.sample_window = NewSampleController(loader, state=state, mutex=mutex, parent=self)
        pass

    def connectUIBehavior(self):
        self.ui.addSampleBtn.clicked.connect(lambda: self.__appendSample())

    def __appendSample(self):
        wdg = SampleController(self.loader, self.sample_window, len(self.children), state=self.state, parent=self)
        self.children[len(self.children)] = wdg
        self._appendWidget(self.ui.listWidget, wdg, self_delete_btn=True, self_clone_btn=True)

    def loadPresets(self):
        for e in TimeUnit.enabled_values():
            self.ui.sampleAfterCmb.addItem(e.pretty_print(), userData=e)
        for e in ImageFormat.enabled_values():
            self.ui.formatCmb.addItem(e.pretty_print(), userData=e)
