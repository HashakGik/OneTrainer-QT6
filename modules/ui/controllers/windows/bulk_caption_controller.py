from modules.ui.controllers.base_controller import BaseController


class BulkCaptionController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/bulk_caption.ui", name=None, parent=parent)