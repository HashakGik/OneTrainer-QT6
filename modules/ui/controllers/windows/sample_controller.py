from modules.ui.controllers.controller_utils import AbstractController

from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

class SampleController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/sample.ui", state=state, name=None, parent=parent)

    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.imagePathBtn, self.ui.imagePathLed, is_dir=False, save=False,
                            title=QCA.translate("dialog_window", "Open Base Image"),
                               filters=QCA.translate("filetype_filters", "Image (*.jpg, *.jpeg, *.tif, *.png, *.webp)"))
        self.connectFileDialog(self.ui.maskPathBtn, self.ui.maskPathLed, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open Mask Image"),
                               filters=QCA.translate("filetype_filters",
                                                     "Image (*.jpg, *.jpeg, *.tif, *.png, *.webp)"))
