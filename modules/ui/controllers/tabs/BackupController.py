from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.BaseController import BaseController

from modules.util.enum.TimeUnit import TimeUnit

from modules.ui.models.TrainingModel import TrainingModel

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

    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/backup.ui", name=QCA.translate("main_window_tabs", "Backup"), parent=parent)
        pass

    def _connectUIBehavior(self):
        self.connect(self.ui.backupCmb.activated, self.__updateBackup(), update_after_connect=True)
        self.connect(self.ui.rollingBackupCbx.toggled, self.__updateRollingBackup(), update_after_connect=True, initial_args=[self.ui.rollingBackupCbx.isChecked()])
        self.connect(self.ui.saveCmb.activated, self.__updateSave(), update_after_connect=True)

        self.connect(self.ui.backupBtn.clicked, self.__backupNow())
        self.connect(self.ui.saveBtn.clicked, self.__saveNow())


    def __backupNow(self):
        def f():
            TrainingModel.instance().backup_now()
        return f

    def __saveNow(self):
        def f():
            TrainingModel.instance().save_now()
        return f

    def __updateBackup(self):
        def f():
            enabled = self.ui.backupCmb.currentData() != TimeUnit.NEVER

            self.ui.backupSbx.setEnabled(enabled)
            self.ui.rollingBackupCbx.setEnabled(enabled)
            self.ui.rollingCountSbx.setEnabled(enabled and self.ui.rollingBackupCbx.isChecked())
            self.ui.rollingCountLbl.setEnabled(enabled and self.ui.rollingBackupCbx.isChecked())

        return f

    def __updateRollingBackup(self):
        def f(enabled):
            self.ui.rollingCountSbx.setEnabled(enabled)
            self.ui.rollingCountLbl.setEnabled(enabled)

        return f

    def __updateSave(self):
        def f():
            enabled = self.ui.saveCmb.currentData() != TimeUnit.NEVER

            self.ui.saveSbx.setEnabled(enabled)
            self.ui.skipSbx.setEnabled(enabled)
            self.ui.rollingCountSbx.setEnabled(enabled)
            self.ui.savePrefixLed.setEnabled(enabled)
            self.ui.skipLbl.setEnabled(enabled)
            self.ui.savePrefixLbl.setEnabled(enabled)

        return f

    def _loadPresets(self):
        for e in TimeUnit.enabled_values():
            self.ui.backupCmb.addItem(e.pretty_print(), userData=e)
        for e in TimeUnit.enabled_values():
            self.ui.saveCmb.addItem(e.pretty_print(), userData=e)

