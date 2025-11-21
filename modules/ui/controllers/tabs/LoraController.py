from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.BaseController import BaseController

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

    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/lora.ui", name=QCA.translate("main_window_tabs", "Lora"), parent=parent)


    def _connectUIBehavior(self):
        self._connectFileDialog(self.ui.baseModelBtn, self.ui.baseModelLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open LoRA/LoHA base model"),
                               filters=QCA.translate("filetype_filters", "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)")) # TODO: Maybe refactor filters in ENUM?

        self.connect(self.ui.typeCmb.activated, self.__updateLora(), update_after_connect=True)
        self.connect(self.ui.decomposeCbx.toggled, self.__updateDora(), update_after_connect=True, initial_args=[self.ui.decomposeCbx.isChecked()])

    def __updateDora(self):
        def f(enabled):
            self.ui.normCbx.setEnabled(enabled)
            self.ui.outputAxisCbx.setEnabled(enabled)
        return f

    def __updateLora(self):
        def f():
            self.ui.doraFrm.setEnabled(self.ui.typeCmb.currentData() == PeftType.LORA)
        return f



    def _connectInputValidation(self):
        # Alpha cannot be higher than rank.
        self.connect(self.ui.rankSbx.valueChanged, lambda x: (self.ui.alphaSbx.setMaximum(x)))


    def _loadPresets(self):
        for e in PeftType.enabled_values():
            self.ui.typeCmb.addItem(e.pretty_print(), userData=e)

        for e in DataType.enabled_values(context="lora"):
            self.ui.weightDTypeCmb.addItem(e.pretty_print(), userData=e)