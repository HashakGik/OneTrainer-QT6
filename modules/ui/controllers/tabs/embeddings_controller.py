from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.util.enum.DataType import DataType

class EmbeddingsController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/embeddings.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "Embeddings"), parent=parent)
        pass

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.baseEmbeddingBtn, self.ui.baseEmbeddingLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open base embeddings"),
                               filters=QCA.translate("filetype_filters", "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)")) # TODO: Maybe refactor filters in ENUM?

    def loadPresets(self):
        for e in DataType.enabled_values(context="embeddings"):
            self.ui.embeddingDTypeCmb.addItem(e.pretty_print(), userData=e)