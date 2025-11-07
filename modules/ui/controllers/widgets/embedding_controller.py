from modules.ui.utils.base_controller import BaseController

from PySide6.QtCore import QCoreApplication as QCA

from modules.util.enum.TimeUnit import TimeUnit

from modules.ui.models.StateModel import StateModel

import PySide6.QtWidgets as QtW

class EmbeddingController(BaseController):
    def __init__(self, loader, idx, parent=None):
        self.idx = idx
        super().__init__(loader, "modules/ui/views/widgets/embedding.ui", name=None, parent=parent)

        # Signal connections here, because idx is needed, and connectUIBehavior() is invoked before self.idx exists.
        self.dynamic_state_ui_connections = {
            "additional_embeddings.{idx}.model_name": "baseEmbeddingLed",
            "additional_embeddings.{idx}.placeholder": "placeholderLed",
            "additional_embeddings.{idx}.token_count": "tokenSbx",
            "additional_embeddings.{idx}.train": "trainCbx",
            "additional_embeddings.{idx}.is_output_embedding": "outputEmbeddingCbx",
            "additional_embeddings.{idx}.stop_training_after": "stopTrainingSbx",
            "additional_embeddings.{idx}.stop_training_after_unit": "stopTrainingCmb",
            "additional_embeddings.{idx}.initial_embedding_text": "initialEmbeddingLed",
        }

        self._connectStateUi(self.dynamic_state_ui_connections, StateModel.instance(), signal=None, idx=self.idx)

        callback = self.__updateEmbedding()
        self.connect(QtW.QApplication.instance().embeddingsChanged, callback)
        callback()



    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.baseEmbeddingBtn, self.ui.baseEmbeddingLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open base embeddings"),
                               filters=QCA.translate("filetype_filters",
                                                     "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)"))


    def __updateEmbedding(self):
        def f():
            self._writeControl(self.ui.baseEmbeddingLed, "additional_embeddings.{}.model_name".format(self.idx), StateModel.instance())
            self._writeControl(self.ui.placeholderLed, "additional_embeddings.{}.placeholder".format(self.idx), StateModel.instance())
            self._writeControl(self.ui.tokenSbx, "additional_embeddings.{}.token_count".format(self.idx), StateModel.instance())
            self._writeControl(self.ui.outputEmbeddingCbx, "additional_embeddings.{}.is_output_embedding".format(self.idx), StateModel.instance())
            self._writeControl(self.ui.stopTrainingSbx, "additional_embeddings.{}.stop_training_after".format(self.idx), StateModel.instance())
            self._writeControl(self.ui.stopTrainingCmb, "additional_embeddings.{}.stop_training_after_unit".format(self.idx), StateModel.instance())
            self._writeControl(self.ui.initialEmbeddingLed, "additional_embeddings.{}.initial_embedding_text".format(self.idx), StateModel.instance())

        return f

    def loadPresets(self):
        for e in TimeUnit.enabled_values():
            self.ui.stopTrainingCmb.addItem(e.pretty_print(), userData=e)