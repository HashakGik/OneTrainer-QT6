from modules.ui.controllers.controller_utils import AbstractController

from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

class SampleController(AbstractController):
    def __init__(self, loader, sample_window, idx, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/widgets/sample.ui", state=state, name=None, parent=parent)
        self.idx = idx
        self.sample_window = sample_window

    def connectUIBehavior(self):
        self.ui.openWindowBtn.clicked.connect(lambda: self.__openSampleWindow())

    def __openSampleWindow(self):
        self.openWindow(self.sample_window, fixed_size=True)
        # TODO: pass to concept_window the state of the current concept