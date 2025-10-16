from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController

from PySide6.QtCore import Slot, Qt
import functools


class LoraController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/lora.ui", state=state, name=QCA.translate("main_window_tabs", "Lora"), parent=parent)
        pass

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.baseModelBtn, self.ui.baseModelLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open LoRA/LoHA base model"),
                               filters=QCA.translate("filetype_filters", "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)")) # TODO: Maybe refactor filters in ENUM?

        self.ui.typeCmb.currentTextChanged.connect(lambda x: self.ui.doraFrm.setEnabled(x == "LoRA"))



    def connectInputValidation(self):
        # Alpha cannot be higher than rank.
        self.ui.rankSbx.valueChanged.connect(lambda x: (self.ui.alphaSbx.setMaximum(x)))