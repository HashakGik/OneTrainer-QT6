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
        for e in NoiseScheduler.enabled_values():
            self.ui.samplerCmb.addItem(e.pretty_print(), userData=e)