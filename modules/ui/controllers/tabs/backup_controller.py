from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController


class BackupController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/backup.ui", state=state, name=QCA.translate("main_window_tabs", "Backup"), parent=parent)
        pass