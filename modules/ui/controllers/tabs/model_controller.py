from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController


class ModelController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/model.ui", state=state, name=QCA.translate("main_window_tabs", "Model"), parent=parent)

    def connectUIBehavior(self):
        # TODO: populate dynamicElementsLay programmatically.

        self.connectFileDialog(self.ui.baseModelBtn, self.ui.baseModelLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open base model"),
                               filters=QCA.translate("filetype_filters",
                                                     "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)"))  # TODO: Maybe refactor filters in ENUM?

        self.connectFileDialog(self.ui.modelOutputBtn, self.ui.modelOutputLed, is_dir=False, save=True,
                               title=QCA.translate("dialog_window", "Save output model"),
                               filters=QCA.translate("filetype_filters",
                                                     "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)"))  # TODO: Maybe refactor filters in ENUM?
