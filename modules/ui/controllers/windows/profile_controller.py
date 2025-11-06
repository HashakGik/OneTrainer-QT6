from modules.ui.utils.base_controller import BaseController


class ProfileController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/profile.ui", name=None, parent=parent)