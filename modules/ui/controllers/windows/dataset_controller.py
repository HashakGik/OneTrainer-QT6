from modules.ui.utils.base_controller import BaseController
from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

from modules.ui.controllers.windows.caption_controller import CaptionController
from modules.ui.controllers.windows.mask_controller import MaskController

class DatasetController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/dataset.ui", name=None, parent=parent)


        self.help_window = QtW.QMessageBox(QtW.QMessageBox.Icon.NoIcon, QCA.translate("dialog_window", "Dataset Tools Help"),
                                 QCA.translate("help_dataset", """
Keyboard shortcuts when focusing on the prompt input field:
Up arrow: previous image
Down arrow: next image
Return: save
Ctrl+M: only show the mask
Ctrl+D: draw mask editing mode
Ctrl+F: fill mask editing mode

When editing masks:
Left click: add mask
Right click: remove mask
Mouse wheel: increase or decrease brush size
"""))
        self.help_window.setModal(False)

        self.dataset = None
        self.mask_window = MaskController(loader, parent=self)
        self.caption_window = CaptionController(loader, parent=self)

    def __openDataset(self):
        diag = QtW.QFileDialog()
        dir = diag.getExistingDirectory(parent=None, caption=QCA.translate("dialog_window", "Open Dataset directory"), dir=self.dataset)

        # TODO: check if dir is a valid dataset folder, then assign:
        self.dataset = dir

    def connectUIBehavior(self):
        self.connect(self.ui.openBtn.clicked, self.__openDataset)
        self.connect(self.ui.generateMaskBtn.clicked, lambda: self.openWindow(self.mask_window, fixed_size=True))
        self.connect(self.ui.generateCaptionsBtn.clicked, lambda: self.openWindow(self.caption_window, fixed_size=True))
        self.connect(self.ui.helpBtn.clicked, lambda: self.help_window.show())