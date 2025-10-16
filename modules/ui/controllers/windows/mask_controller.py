from modules.ui.controllers.controller_utils import AbstractController

from PySide6.QtCore import QCoreApplication as QCA

class MaskController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/generate_mask.ui", state=state, name=None, parent=parent)

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.folderBtn, self.ui.folderLed, is_dir=True, save=False, title=
                               QCA.translate("dialog_window", "Open Dataset directory"))