from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController


class ConvertController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/convert.ui", state=state, name=None, parent=parent)

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.inputBtn, self.ui.inputLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open Input model"),
                               filters=QCA.translate("filetype_filters", "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)"))
        self.connectFileDialog(self.ui.outputBtn, self.ui.outputLed, is_dir=False, save=True,
                               title=QCA.translate("dialog_window", "Save Output model"),
                               filters=QCA.translate("filetype_filters", "Safetensors (*.safetensors);;Diffusers (model_index.json)"))