from modules.ui.controllers.BaseController import BaseController


class BulkCaptionController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/bulk_caption.ui", name=None, parent=parent)