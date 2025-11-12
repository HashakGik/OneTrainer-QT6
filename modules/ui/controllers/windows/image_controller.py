from modules.ui.controllers.base_controller import BaseController


class ImageController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/image.ui", name=None, parent=parent)