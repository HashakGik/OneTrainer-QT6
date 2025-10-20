from modules.ui.utils.base_controller import BaseController

from PySide6.QtCore import QCoreApplication as QCA


class SampleController(BaseController):
    def __init__(self, loader, sample_window, idx, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/widgets/sample.ui", state=state, mutex=mutex, name=None, parent=parent)
        self.idx = idx
        self.sample_window = sample_window

    def connectUIBehavior(self):
        self.ui.openWindowBtn.clicked.connect(lambda: self.__openSampleWindow())

    def __openSampleWindow(self):
        self.openWindow(self.sample_window, fixed_size=True)
        # TODO: pass to concept_window the state of the current concept