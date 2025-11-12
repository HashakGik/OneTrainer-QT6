from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.base_controller import BaseController

from modules.ui.controllers.windows.dataset_controller import DatasetController
from modules.ui.controllers.windows.image_controller import ImageController
from modules.ui.controllers.windows.bulk_caption_controller import BulkCaptionController
from modules.ui.controllers.windows.video_controller import VideoController
from modules.ui.controllers.windows.convert_controller import ConvertController
from modules.ui.controllers.windows.sample_controller import SampleController
from modules.ui.controllers.windows.profile_controller import ProfileController

import PySide6.QtWidgets as QtW

class ToolsController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/tools.ui", name=QCA.translate("main_window_tabs", "Tools"), parent=parent)


        self.children = {"dataset": DatasetController(loader, parent=None),
                         "image": ImageController(loader, parent=None),
                         "bulk_caption": BulkCaptionController(loader, parent=None),
                        "video": VideoController(loader, parent=None),
                        "convert": ConvertController(loader, parent=None),
                        "sample": SampleController(loader, parent=None),
                        "profile": ProfileController(loader, parent=None)}


    def __open(self, window):
        if self.children[window].ui.isHidden():
            if window == "sample":
                QtW.QApplication.instance().openSample.emit(-1)

            self.openWindow(self.children[window], fixed_size=window != "dataset")
        else:
            self.children[window].ui.activateWindow()

    def connectUIBehavior(self):
        self.connect(self.ui.datasetBtn.clicked, lambda: self.__open("dataset"))
        self.connect(self.ui.imageBtn.clicked, lambda: self.__open("image"))
        self.connect(self.ui.bulkCaptionBtn.clicked, lambda: self.__open("bulk_caption"))
        self.connect(self.ui.videoBtn.clicked, lambda: self.__open("video"))
        self.connect(self.ui.convertBtn.clicked, lambda: self.__open("convert"))
        self.connect(self.ui.samplingBtn.clicked, lambda: self.__open("sample"))
        self.connect(self.ui.profilingBtn.clicked, lambda: self.__open("profile"))