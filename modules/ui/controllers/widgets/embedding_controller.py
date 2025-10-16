from modules.ui.controllers.controller_utils import AbstractController

from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

class EmbeddingController(AbstractController):
    def __init__(self, loader, idx, state=None, parent=None):
        super().__init__(loader, "modules/ui/widgets/embedding.ui", state=state, name=None, parent=parent)
        self.idx = idx
