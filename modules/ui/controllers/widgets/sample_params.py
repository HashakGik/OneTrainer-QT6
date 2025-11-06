from modules.ui.utils.base_controller import BaseController

from modules.util.enum.NoiseScheduler import NoiseScheduler

from modules.ui.models.SampleModel import SampleModel

from PySide6.QtCore import QCoreApplication as QCA

import PySide6.QtWidgets as QtW

class SampleParamsController(BaseController):
    idx = 0
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/widgets/sampling_params.ui", name=None, parent=parent)


    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.imagePathBtn, self.ui.imagePathLed, is_dir=False, save=False,
                            title=QCA.translate("dialog_window", "Open Base Image"),
                               filters=QCA.translate("filetype_filters", "Image (*.jpg, *.jpeg, *.tif, *.png, *.webp)"))
        self.connectFileDialog(self.ui.maskPathBtn, self.ui.maskPathLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open Mask Image"),
                               filters=QCA.translate("filetype_filters",
                                                     "Image (*.jpg, *.jpeg, *.tif, *.png, *.webp)"))

        QtW.QApplication.instance().openSample.connect(self.__updateSample())
        # TODO: THIS IS A CLASSIC WINDOW, NO NEED TO CONNECT ANYTHING IN READ/WRITE. PARENTS WILL READ DATA AND DECIDE WHAT TO DO WITH IT

    def __updateSample(self):
        def f(idx):

            if idx >= 0 and idx < len(SampleModel.instance()):
                self.idx = idx
                self._writeControl(self.ui.promptLed, "{}.prompt".format(idx), SampleModel.instance())
                self._writeControl(self.ui.negativePromptLed, "{}.negative_prompt".format(idx), SampleModel.instance())
                self._writeControl(self.ui.widthSbx, "{}.width".format(idx), SampleModel.instance())
                self._writeControl(self.ui.heightSbx, "{}.height".format(idx), SampleModel.instance())
                self._writeControl(self.ui.framesSbx, "{}.frames".format(idx), SampleModel.instance())
                self._writeControl(self.ui.lengthSbx, "{}.length".format(idx), SampleModel.instance())
                self._writeControl(self.ui.seedSbx, "{}.seed".format(idx), SampleModel.instance())
                self._writeControl(self.ui.randomSeedCbx, "{}.random_seed".format(idx), SampleModel.instance())
                self._writeControl(self.ui.cfgSbx, "{}.cfg_scale".format(idx), SampleModel.instance())
                self._writeControl(self.ui.stepsSbx, "{}.diffusion_steps".format(idx), SampleModel.instance())
                self._writeControl(self.ui.samplerCmb, "{}.noise_scheduler".format(idx), SampleModel.instance())
                self._writeControl(self.ui.inpaintingCbx, "{}.sample_inpainting".format(idx), SampleModel.instance())
                self._writeControl(self.ui.imagePathLed, "{}.base_image_path".format(idx), SampleModel.instance())
                self._writeControl(self.ui.maskPathLed, "{}.mask_image_path".format(idx), SampleModel.instance())
            else:
                # There is no need to acquire the lock for these values, as they are read-only defaults.
                default_sample = SampleModel.instance().get_default_sample()
                self.ui.promptLed.setText(default_sample["prompt"])
                self.ui.negativePromptLed.setText(default_sample["negative_prompt"])
                self.ui.widthSbx.setValue(default_sample["width"])
                self.ui.heightSbx.setValue(default_sample["height"])
                self.ui.framesSbx.setValue(default_sample["frames"])
                self.ui.lengthSbx.setValue(default_sample["length"])
                self.ui.seedSbx.setValue(default_sample["seed"])
                self.ui.randomSeedCbx.setChecked(default_sample["random_seed"])
                self.ui.cfgSbx.setValue(default_sample["cfg_scale"])
                self.ui.stepsSbx.setValue(default_sample["diffusion_steps"])

                idx = self.ui.samplerCmb.findData(default_sample["noise_scheduler"])
                if idx != -1:
                    self.ui.samplerCmb.setCurrentIndex(idx)

                self.ui.inpaintingCbx.setChecked(default_sample["sample_inpainting"])
                self.ui.imagePathLed.setText(default_sample["base_image_path"])
                self.ui.maskPathLed.setText(default_sample["mask_image_path"])
        return f

    def loadPresets(self):
        for e in NoiseScheduler.enabled_values():
            self.ui.samplerCmb.addItem(e.pretty_print(), userData=e)