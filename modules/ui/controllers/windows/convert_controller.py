from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.util.enum.ModelType import ModelType
from modules.util.enum.TrainingMethod import TrainingMethod
from modules.util.enum.DataType import DataType
from modules.util.enum.ModelFormat import ModelFormat

class ConvertController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/convert.ui", state=state, mutex=mutex, name=None, parent=parent)

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.inputBtn, self.ui.inputLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open Input model"),
                               filters=QCA.translate("filetype_filters", "Safetensors (*.safetensors);;Diffusers (model_index.json);;Checkpoints (*.ckpt, *.pt, *.bin);;All Files (*.*)"))
        self.connectFileDialog(self.ui.outputBtn, self.ui.outputLed, is_dir=False, save=True,
                               title=QCA.translate("dialog_window", "Save Output model"),
                               filters=QCA.translate("filetype_filters", "Safetensors (*.safetensors);;Diffusers (model_index.json)"))

    def loadPresets(self):
        for k, v in {
            "Stable Diffusion 1.5": ModelType.STABLE_DIFFUSION_15,
            "Stable Diffusion 1.5 Inpainting": ModelType.STABLE_DIFFUSION_15_INPAINTING,
            "Stable Diffusion 2.0": ModelType.STABLE_DIFFUSION_20,
            "Stable Diffusion 2.0 Inpainting": ModelType.STABLE_DIFFUSION_20_INPAINTING,
            "Stable Diffusion 2.1": ModelType.STABLE_DIFFUSION_21,
            "Stable Diffusion 3": ModelType.STABLE_DIFFUSION_3,
            "Stable Diffusion 3.5": ModelType.STABLE_DIFFUSION_35,
            "Stable Diffusion XL 1.0 Base": ModelType.STABLE_DIFFUSION_XL_10_BASE,
            "Stable Diffusion XL 1.0 Base Inpainting": ModelType.STABLE_DIFFUSION_XL_10_BASE_INPAINTING,
            "Wuerstchen v2": ModelType.WUERSTCHEN_2,
            "Stable Cascade": ModelType.STABLE_CASCADE_1,
            "PixArt Alpha": ModelType.PIXART_ALPHA,
            "PixArt Sigma": ModelType.PIXART_SIGMA,
            "Flux Dev": ModelType.FLUX_DEV_1,
            "Flux Fill Dev": ModelType.FLUX_FILL_DEV_1,
            "Hunyuan Video": ModelType.HUNYUAN_VIDEO,
            "Chroma1": ModelType.CHROMA_1,  # TODO does this just work? HiDream is not here
            "QwenImage": ModelType.QWEN,  # TODO does this just work? HiDream is not here
        }.items():
            self.ui.modelTypeCmb.addItem(k, userData=v)

        for k, v in {
            "Base Model": TrainingMethod.FINE_TUNE,
            "LoRA": TrainingMethod.LORA,
            "Embedding": TrainingMethod.EMBEDDING
        }.items():
            self.ui.trainingMethodCmb.addItem(k, userData=v)

        for k, v in {
            "float32": DataType.FLOAT_32,
            "float16": DataType.FLOAT_16,
            "bfloat16": DataType.BFLOAT_16
        }.items():
            self.ui.outputDTypeCmb.addItem(k, userData=v)

        for k, v in {
            "Safetensors": ModelFormat.SAFETENSORS,
            "Diffusers": ModelFormat.DIFFUSERS,
        }.items():
            self.ui.outputFormatCmb.addItem(k, userData=v)


        pass