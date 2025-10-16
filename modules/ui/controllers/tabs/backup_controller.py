from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController

from modules.util.enum.TimeUnit import TimeUnit

class BackupController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/backup.ui", state=state, name=QCA.translate("main_window_tabs", "Backup"), parent=parent)
        pass

    def connectUIBehavior(self):
        # TODO: if never disable stuff...
        pass

    def loadPresets(self):
        for e in TimeUnit:
            self.ui.backupCmb.addItem(self._prettyPrint(e.value), userData=e)
        for e in TimeUnit:
            self.ui.saveCmb.addItem(self._prettyPrint(e.value), userData=e)

