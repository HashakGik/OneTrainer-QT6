from modules.ui.utils.base_controller import BaseController

from PySide6.QtCore import QCoreApplication as QCA

class MaskController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/generate_mask.ui", state=state, mutex=mutex, name=None, parent=parent)

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.folderBtn, self.ui.folderLed, is_dir=True, save=False, title=
                               QCA.translate("dialog_window", "Open Dataset directory"))

    def loadPresets(self):
        for e in ["ClipSeg", "Rembg", "Rembg-Human", "Hex Color"]:
            self.ui.modelCmb.addItem(e, userData=e)

        for k, v in {
            "Replace all masks": "replace",
            "Create if absent": "fill",
            "Add to existing": "add",
            "Subtract from existing": "subtract",
            "Blend with existing": "blend"
        }.items():
            self.ui.modeCmb.addItem(k, userData=v)

        pass