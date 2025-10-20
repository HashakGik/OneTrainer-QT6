from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.util.enum.TimeUnit import TimeUnit

class BackupController(BaseController):
    state_ui_connections = {
        "backup_after": "backupSbx",
        "backup_after_unit": "backupCmb",
        "rolling_backup": "rollingBackupCbx",
        "backup_before_save": "backupBeforeSaveCbx",
        "rolling_backup_count": "rollingCountSbx",
        "save_every": "saveSbx",
        "save_every_unit": "saveCmb",
        "save_skip_first": "skipSbx",
        "save_filename_prefix": "savePrefixLed"
    }

    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/backup.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "Backup"), parent=parent)
        pass

    def connectUIBehavior(self):
        # TODO: if never disable stuff...
        pass

    def loadPresets(self):
        for e in TimeUnit:
            self.ui.backupCmb.addItem(self._prettyPrint(e.value), userData=e)
        for e in TimeUnit:
            self.ui.saveCmb.addItem(self._prettyPrint(e.value), userData=e)

