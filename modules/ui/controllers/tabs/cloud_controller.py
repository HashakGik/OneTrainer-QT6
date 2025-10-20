from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.util.enum.CloudAction import CloudAction
from modules.util.enum.CloudType import CloudType
from modules.util.enum.CloudFileSync import CloudFileSync

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

    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/cloud.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "Cloud"), parent=parent)


    def loadPresets(self):
        for ctl in [self.ui.onFinishCmb, self.ui.onErrorCmb, self.ui.onDetachedCmb, self.ui.onDetachedErrorCmb]:
            for e in CloudAction:
                ctl.addItem(self._prettyPrint(e.value), userData=e)

        for e in CloudType:
            self.ui.cloudTypeCmb.addItem(self._prettyPrint(e.value), userData=e)

        for e in CloudFileSync:
            self.ui.fileSyncMethodCmb.addItem(self._prettyPrint(e.value), userData=e)

        # subTypeCmb has no enum on original code. Adding manually.
        for e in ["", "COMMUNITY", "SECURE"]:
            self.ui.subTypeCmb.addItem(self._prettyPrint(e), userData=e)