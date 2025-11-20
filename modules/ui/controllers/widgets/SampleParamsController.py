from modules.ui.controllers.BaseController import BaseController

from modules.util.enum.NoiseScheduler import NoiseScheduler

from modules.ui.models.SampleModel import SampleModel

from PySide6.QtCore import QCoreApplication as QCA

import PySide6.QtWidgets as QtW

class SampleParamsController(BaseController):
    idx = 0
    def __init__(self, loader, model_instance, update_signal=None, use_idx=False, parent=None):
        self.model_instance = model_instance
        self.use_idx = use_idx
        self.update_signal = update_signal

        super().__init__(loader, "modules/ui/views/widgets/sampling_params.ui", name=None, parent=parent)


    def _connectUIBehavior(self):
        self._connectFileDialog(self.ui.imagePathBtn, self.ui.imagePathLed, is_dir=False, save=False,
                            title=QCA.translate("dialog_window", "Open Base Image"),
                               filters=QCA.translate("filetype_filters", "Image (*.jpg, *.jpeg, *.tif, *.png, *.webp)"))
        self._connectFileDialog(self.ui.maskPathBtn, self.ui.maskPathLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open Mask Image"),
                               filters=QCA.translate("filetype_filters",
                                                     "Image (*.jpg, *.jpeg, *.tif, *.png, *.webp)"))

        self.dynamic_state_ui_connections = {
            "prompt": "promptLed",
            "negative_prompt": "negativePromptLed",
            "width": "widthSbx",
            "height": "heightSbx",
            "frames": "framesSbx",
            "length": "lengthSbx",
            "seed": "seedSbx",
            "random_seed": "randomSeedCbx",
            "cfg_scale": "cfgSbx",
            "diffusion_steps": "stepsSbx",
            "noise_scheduler": "samplerCmb",
            "sample_inpainting": "inpaintingCbx",
            "base_image_path": "imagePathLed",
            "mask_image_path": "maskPathLed",
        }
        if self.use_idx:
            self.dynamic_state_ui_connections = {"{{idx}}.{}".format(k): v for k, v in self.dynamic_state_ui_connections.items()}

        if self.update_signal is not None: # If we have a dynamic connection, we connect the signal to the update.
            self.connect(self.update_signal, self.__reconnectControls())
        else:
            self.__reconnectControls()() # In case we have a static connection, we update now instead.


    def __reconnectControls(self):
        def f(idx=None):
            if self.use_idx:
                self.disconnectGroup("idx")
                self._connectStateUi(self.dynamic_state_ui_connections, self.model_instance, signal=self.update_signal, group="idx", update_after_connect=True, idx=idx)
            else:
                self._connectStateUi(self.dynamic_state_ui_connections, self.model_instance, update_after_connect=True, signal=self.update_signal)
        return f

    def _loadPresets(self):
        for e in NoiseScheduler.enabled_values():
            self.ui.samplerCmb.addItem(e.pretty_print(), userData=e)