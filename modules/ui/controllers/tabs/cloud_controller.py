from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController

from modules.util.enum.CloudAction import CloudAction
from modules.util.enum.CloudType import CloudType
from modules.util.enum.CloudFileSync import CloudFileSync

class CloudController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/cloud.ui", state=state, name=QCA.translate("main_window_tabs", "Cloud"), parent=parent)


    def loadPresets(self):
        for ctl in [self.ui.onFinishCmb, self.ui.onErrorCmb, self.ui.onDetachedCmb, self.ui.onDetachedErrorCmb]:
            for e in CloudAction:
                ctl.addItem(self._prettyPrint(e.value), userData=e)

        for e in CloudType:
            self.ui.cloudTypeCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in CloudFileSync:
            self.ui.fileSyncMethodCmb.addItem(self._prettyPrint(e.value), userData=e)

        # subTypeCmb has no enum on original code. Adding manually.
        for e in ["", "COMMUNITY", "SECURE"]:
            self.ui.subTypeCmb.addItem(self._prettyPrint(e), userData=e)