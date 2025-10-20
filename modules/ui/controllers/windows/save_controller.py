from modules.ui.utils.base_controller import BaseController


class SaveController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/save.ui", state=state, mutex=mutex, name=None, parent=parent)
