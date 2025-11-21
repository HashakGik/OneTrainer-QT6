from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.BaseController import BaseController


class DataController(BaseController):
    state_ui_connections = {
        "aspect_ratio_bucketing": "aspectBucketingCbx",
        "latent_caching": "latentCachingCbx",
        "clear_cache_before_training": "clearCacheCbx"
    }

    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/data.ui", name=QCA.translate("main_window_tabs", "Data"), parent=parent)


    def _connectUIBehavior(self):
        self.connect(self.ui.latentCachingCbx.toggled, self.__updateCaching(), update_after_connect=True, initial_args=[self.ui.latentCachingCbx.isChecked()])

    def __updateCaching(self):
        def f(enabled):
            self.ui.clearCacheCbx.setEnabled(enabled)
        return f