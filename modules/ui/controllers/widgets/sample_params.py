from modules.ui.utils.base_controller import BaseController

from modules.util.enum.NoiseScheduler import NoiseScheduler

from PySide6.QtCore import QCoreApplication as QCA


class SampleParamsController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/widgets/sampling_params.ui", state=state, mutex=mutex, name=None, parent=parent)


    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.imagePathBtn, self.ui.imagePathLed, is_dir=False, save=False,
                            title=QCA.translate("dialog_window", "Open Base Image"),
                               filters=QCA.translate("filetype_filters", "Image (*.jpg, *.jpeg, *.tif, *.png, *.webp)"))
        self.connectFileDialog(self.ui.maskPathBtn, self.ui.maskPathLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open Mask Image"),
                               filters=QCA.translate("filetype_filters",
                                                     "Image (*.jpg, *.jpeg, *.tif, *.png, *.webp)"))

    def loadPresets(self):
        for k, v in {
            "DDIM": NoiseScheduler.DDIM,
            "Euler": NoiseScheduler.EULER,
            "Euler A": NoiseScheduler.EULER_A,
            # "DPM++": NoiseScheduler.DPMPP, # TODO: produces noisy samples
            # "DPM++ SDE": NoiseScheduler.DPMPP_SDE, # TODO: produces noisy samples
            "UniPC": NoiseScheduler.UNIPC,
            "Euler Karras": NoiseScheduler.EULER_KARRAS,
            "DPM++ Karras": NoiseScheduler.DPMPP_KARRAS,
            "DPM++ SDE Karras": NoiseScheduler.DPMPP_SDE_KARRAS,
            # "UniPC Karras": NoiseScheduler.UNIPC_KARRAS # TODO: update diffusers to fix UNIPC_KARRAS (see https://github.com/huggingface/diffusers/pull/4581)
        }.items():
            self.ui.samplerCmb.addItem(k, userData=v)