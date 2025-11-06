from modules.ui.utils.base_controller import BaseController
from PySide6.QtCore import QCoreApplication as QCA

from modules.util.enum.GenerateCaptionsModel import GenerateCaptionsModel, GenerateCaptionsAction

class CaptionController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/generate_caption.ui", name=None, parent=parent)

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.folderBtn, self.ui.folderLed, is_dir=True, save=False, title=
                               QCA.translate("dialog_window", "Open Dataset directory"))

    def loadPresets(self):
        for e in GenerateCaptionsModel.enabled_values():
            self.ui.modelCmb.addItem(e.pretty_print(), userData=e)

        for e in GenerateCaptionsAction.enabled_values():
            self.ui.modeCmb.addItem(e.pretty_print(), userData=e)
