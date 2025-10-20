from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController
import PySide6.QtWidgets as QtW

from modules.util.enum.DataType import DataType
from modules.util.enum.ModelType import PeftType

class LoraController(BaseController):
    state_ui_connections = {
        "peft_type": "typeCmb",
        "lora_model_name": "baseModelLed",
        "lora_rank": "rankSbx",
        "lora_alpha": "alphaSbx",
        "lora_decompose": "decomposeCbx",
        "lora_decompose_norm_epsilon": "normCbx",
        "lora_decompose_output_axis": "outputAxisCbx",
        "lora_weight_dtype": "weightDTypeCmb",
        "bundle_additional_embeddings": "bundleCbx"
    }

    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/lora.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "Lora"), parent=parent)


    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.baseModelBtn, self.ui.baseModelLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open LoRA/LoHA base model"),
                               filters=QCA.translate("filetype_filters", "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)")) # TODO: Maybe refactor filters in ENUM?

        self.ui.typeCmb.activated.connect(lambda: self.ui.doraFrm.setEnabled(self.ui.typeCmb.currentData() == PeftType.LORA))



    def connectInputValidation(self):
        # Alpha cannot be higher than rank.
        self.ui.rankSbx.valueChanged.connect(lambda x: (self.ui.alphaSbx.setMaximum(x)))


    def loadPresets(self):
        for e in PeftType:
            self.ui.typeCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in [DataType.FLOAT_32, DataType.BFLOAT_16]:
            self.ui.weightDTypeCmb.addItem(self._prettyPrint(e.value), userData=e)