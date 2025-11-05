from modules.ui.utils.base_controller import BaseController

from PySide6.QtCore import QCoreApplication as QCA

from modules.util.enum.TimeUnit import TimeUnit

class EmbeddingController(BaseController):
    def __init__(self, loader, idx, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/widgets/embedding.ui", state=state, mutex=mutex, name=None, parent=parent)
        self.idx = idx

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.baseEmbeddingBtn, self.ui.baseEmbeddingLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open base embeddings"),
                               filters=QCA.translate("filetype_filters",
                                                     "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)"))

    def loadPresets(self):
        for e in TimeUnit.enabled_values():
            self.ui.stopTrainingCmb.addItem(e.pretty_print(), userData=e)