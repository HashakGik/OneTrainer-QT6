from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController
from modules.util.enum.TimeUnit import TimeUnit

from modules.util.enum.GradientReducePrecision import GradientReducePrecision

class GeneralController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/general.ui", state=state, name=QCA.translate("main_window_tabs", "General"), parent=parent)


    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.workspaceBtn, self.ui.workspaceLed, is_dir=True, save=False,
                               title=QCA.translate("dialog_window", "Open Workspace directory"))
        self.connectFileDialog(self.ui.cacheBtn, self.ui.cacheLed, is_dir=True, save=False,
                               title=QCA.translate("dialog_window", "Open Cache directory"))
        self.connectFileDialog(self.ui.debugBtn, self.ui.debugLed, is_dir=True, save=False,
                               title=QCA.translate("dialog_window", "Open Debug directory"))

    def loadPresets(self):
        for e in GradientReducePrecision:
            self.ui.gradientReduceCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in TimeUnit:
            self.ui.validateCmb.addItem(self._prettyPrint(e.value), userData=e)
        pass