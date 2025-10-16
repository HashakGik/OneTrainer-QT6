from modules.ui.controllers.controller_utils import AbstractController


class OptimizerController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/optimizer.ui", state=state, name=None, parent=parent)