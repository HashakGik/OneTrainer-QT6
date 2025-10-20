from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController


class DataController(BaseController):
    state_ui_connections = {
        "aspect_ratio_bucketing": "aspectBucketingCbx",
        "latent_caching": "latentCachingCbx",
        "clear_cache_before_training": "clearCacheCbx"
    }

    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/data.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "Data"), parent=parent)
