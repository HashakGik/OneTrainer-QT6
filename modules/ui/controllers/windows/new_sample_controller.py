from modules.ui.utils.base_controller import BaseController
from modules.ui.controllers.widgets.sample_params import SampleParamsController


from modules.ui.models.SampleModel import SampleModel

import PySide6.QtWidgets as QtW


class NewSampleController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/new_sample.ui", name=None, parent=parent)

        self.samplingParams = SampleParamsController(loader, parent=parent)
        self.ui.paramsLay.addWidget(self.samplingParams.ui)

    def connectUIBehavior(self):
        self.connect(self.ui.okBtn.clicked, self.__saveSample())

    def __saveSample(self):
        def f():
            SampleModel.instance().setState("{}.prompt".format(self.samplingParams.idx), self.samplingParams.ui.promptLed.text())
            SampleModel.instance().setState("{}.negative_prompt".format(self.samplingParams.idx), self.samplingParams.ui.negativePromptLed.text())
            SampleModel.instance().setState("{}.width".format(self.samplingParams.idx), self.samplingParams.ui.widthSbx.value())
            SampleModel.instance().setState("{}.height".format(self.samplingParams.idx), self.samplingParams.ui.heightSbx.value())
            SampleModel.instance().setState("{}.frames".format(self.samplingParams.idx), self.samplingParams.ui.framesSbx.value())
            SampleModel.instance().setState("{}.length".format(self.samplingParams.idx), self.samplingParams.ui.lengthSbx.value())
            SampleModel.instance().setState("{}.seed".format(self.samplingParams.idx), self.samplingParams.ui.seedSbx.value())
            SampleModel.instance().setState("{}.random_seed".format(self.samplingParams.idx), self.samplingParams.ui.randomSeedCbx.isChecked())
            SampleModel.instance().setState("{}.cfg_scale".format(self.samplingParams.idx), self.samplingParams.ui.cfgSbx.value())
            SampleModel.instance().setState("{}.diffusion_steps".format(self.samplingParams.idx), self.samplingParams.ui.stepsSbx.value())
            SampleModel.instance().setState("{}.noise_scheduler".format(self.samplingParams.idx), self.samplingParams.ui.samplerCmb.currentData())
            SampleModel.instance().setState("{}.sample_inpainting".format(self.samplingParams.idx), self.samplingParams.ui.inpaintingCbx.isChecked())
            SampleModel.instance().setState("{}.base_image_path".format(self.samplingParams.idx), self.samplingParams.ui.imagePathLed.text())
            SampleModel.instance().setState("{}.mask_image_path".format(self.samplingParams.idx), self.samplingParams.ui.maskPathLed.text())

            QtW.QApplication.instance().samplesChanged.emit()
            self.ui.hide()

        return f