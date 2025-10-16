from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController


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
