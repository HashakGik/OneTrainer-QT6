from PySide6.QtCore import QCoreApplication as QCA

from modules.ui.controllers.BaseController import BaseController

from modules.util.enum.CloudAction import CloudAction
from modules.util.enum.CloudType import CloudType
from modules.util.enum.CloudSubtype import CloudSubtype
from modules.util.enum.CloudFileSync import CloudFileSync

from modules.ui.models.StateModel import StateModel
from modules.ui.models.TrainingModel import TrainingModel

class CloudController(BaseController):
    state_ui_connections = {
        "cloud.enabled": "enabledCbx",
        "cloud.type": "cloudTypeCmb",
        "cloud.file_sync": "fileSyncMethodCmb",
        "secrets.cloud.api_key": "apiKeyLed",
        "secrets.cloud.host": "hostnameLed",
        "secrets.cloud.port": "portSbx",
        "secrets.cloud.user": "userLed",
        "secrets.cloud.id": "cloudIdLed",
        "cloud.tensorboard_tunnel": "tensorboardTcpTunnelCbx",
        "cloud.detach_trainer": "detachRemoteTrainerCbx",
        "cloud.run_id": "reattachIdLed",
        "cloud.download_samples": "downloadSamplesCbx",
        "cloud.download_output_model": "downloadOutputModelCbx",
        "cloud.download_saves": "downloadSavedCheckpointsCbx",
        "cloud.download_backups": "downloadBackupsCbx",
        "cloud.download_tensorboard": "downloadTensorboardLogCbx",
        "cloud.delete_workspace": "deleteRemoteWorkspaceCbx",
        "cloud.remote_dir": "remoteDirectoryLed",
        "cloud.onetrainer_dir": "onetrainerDirectoryLed",
        "cloud.huggingface_cache_dir": "huggingfaceCacheLed",
        "cloud.install_onetrainer": "installOnetrainerCbx",
        "cloud.install_cmd": "installCommandLed",
        "cloud.update_onetrainer": "updateOnetrainerCbx",
        "cloud.create": "createCloudCbx",
        "cloud.name": "cloudNameLed",
        "cloud.sub_type": "subTypeCmb",
        "cloud.gpu_type": "gpuCmb",
        "cloud.volume_size": "volumeSizeSbx",
        "cloud.min_download": "minDownloadSbx",
        "cloud.on_finish": "onFinishCmb",
        "cloud.on_error": "onErrorCmb",
        "cloud.on_detached_finish": "onDetachedCmb",
        "cloud.on_detached_error": "onDetachedErrorCmb",
    }

    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/cloud.ui", name=QCA.translate("main_window_tabs", "Cloud"), parent=parent)


    def _connectUIBehavior(self):
        self.connect(self.ui.createCloudBtn.clicked, self.__createCloud())
        self.connect(self.ui.gpuBtn.clicked, self.__getGPUTypes())
        self.connect(self.ui.reattachBtn.clicked, self.__reattach())

        self.connect(self.ui.enabledCbx.toggled, self.ui.frame.setEnabled)

    def __reattach(self):
        def f():
            TrainingModel.instance().reattach()
        return f

    def __getGPUTypes(self):
        def f():
            self.ui.gpuCmb.clear()
            for gpu in StateModel.instance().get_gpus():
                self.ui.gpuCmb.addItem(gpu.name, userData=gpu)

        return f

    def __createCloud(self):
        def f():
            if StateModel.instance().getState("cloud.type") == CloudType.RUNPOD:
                self.openUrl("https://www.runpod.io/console/deploy?template=1a33vbssq9&type=gpu")
        return f


    def _loadPresets(self):
        for ctl in [self.ui.onFinishCmb, self.ui.onErrorCmb, self.ui.onDetachedCmb, self.ui.onDetachedErrorCmb]:
            for e in CloudAction.enabled_values():
                ctl.addItem(e.pretty_print(), userData=e)

        for e in CloudType.enabled_values():
            self.ui.cloudTypeCmb.addItem(e.pretty_print(), userData=e)

        for e in CloudFileSync.enabled_values():
            self.ui.fileSyncMethodCmb.addItem(e.pretty_print(), userData=e)

        for e in CloudSubtype.enabled_values():
            self.ui.subTypeCmb.addItem(e.pretty_print(), userData=e)