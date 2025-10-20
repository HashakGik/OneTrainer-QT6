from modules.ui.utils.base_controller import BaseController
from PySide6.QtCore import QCoreApplication as QCA

class CaptionController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/generate_caption.ui", state=state, mutex=mutex, name=None, parent=parent)

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.folderBtn, self.ui.folderLed, is_dir=True, save=False, title=
                               QCA.translate("dialog_window", "Open Dataset directory"))

    def loadPresets(self):
        for e in ["Blip", "Blip2", "WD14 VIT v2"]:
            self.ui.modelCmb.addItem(e, userData=e)

            for e in ["Replace all captions", "Create if absent", "Add as new line"]:
                self.ui.modeCmb.addItem(e, userData=e)