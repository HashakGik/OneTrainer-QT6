from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController
from modules.util.enum.TimeUnit import TimeUnit

from modules.util.enum.GradientReducePrecision import GradientReducePrecision

class GeneralController(BaseController):
    state_ui_connections = {
        "workspace_dir": "workspaceLed",
        "continue_last_backup": "continueCbx",
        "debug_mode": "debugCbx",
        "tensorboard": "tensorboardCbx",
        "tensorboard_expose": "exposeTensorboardCbx",
        "validation": "validateCbx",
        "dataloader_threads": "dataloaderSbx",
        "train_device": "trainDeviceLed",
        "multi_gpu": "multiGpuCbx",
        "sequential_model_setup": "sequentialCbx",
        "gradient_reduce_precision": "gradientReduceCmb",
        "async_gradient_reduce": "asyncGradientCbx",
        "temp_device": "tempDeviceLed",
        "cache_dir": "cacheLed",
        "only_cache": "onlyCacheCbx",
        "debug_dir": "debugLed",
        "tensorboard_always_on": "alwaysOnTensorboardCbx",
        "tensorboard_port": "tensorboardSbx",
        "validate_after": "validateSbx",
        "validate_after_unit": "validateCmb",
        "device_indexes": "deviceIndexesLed",
        "fused_gradient_reduce": "fusedGradientCbx",
        "async_gradient_reduce_buffer": "bufferSbx",
    }

    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/general.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "General"), parent=parent)


    def connectUIBehavior(self):
        self.connectFileDialog(self.ui.workspaceBtn, self.ui.workspaceLed, is_dir=True, save=False,
                               title=QCA.translate("dialog_window", "Open Workspace directory"))
        self.connectFileDialog(self.ui.cacheBtn, self.ui.cacheLed, is_dir=True, save=False,
                               title=QCA.translate("dialog_window", "Open Cache directory"))
        self.connectFileDialog(self.ui.debugBtn, self.ui.debugLed, is_dir=True, save=False,
                               title=QCA.translate("dialog_window", "Open Debug directory"))

    def loadPresets(self):
        for e in GradientReducePrecision:
            self.ui.gradientReduceCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in TimeUnit:
            self.ui.validateCmb.addItem(self._prettyPrint(e.value), userData=e)
        pass