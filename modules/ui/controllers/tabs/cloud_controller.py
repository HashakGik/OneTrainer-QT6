from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController


class CloudController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/cloud.ui", state=state, name=QCA.translate("main_window_tabs", "Cloud"), parent=parent)
        pass
        # TODO: Rename controls in UI!
