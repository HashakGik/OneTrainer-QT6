from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.BaseController import BaseController

from modules.ui.controllers.windows.DatasetController import DatasetController
from modules.ui.controllers.windows.ImageController import ImageController
from modules.ui.controllers.windows.BulkCaptionController import BulkCaptionController
from modules.ui.controllers.windows.VideoController import VideoController
from modules.ui.controllers.windows.ConvertController import ConvertController
from modules.ui.controllers.windows.SampleController import SampleController
from modules.ui.controllers.windows.ProfileController import ProfileController

import PySide6.QtWidgets as QtW

class ToolsController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/tools.ui", name=QCA.translate("main_window_tabs", "Tools"), parent=parent)

    def _setup(self):

        self.children = {"dataset": DatasetController(self.loader, parent=None),
                         "image": ImageController(self.loader, parent=None),
                         "bulk_caption": BulkCaptionController(self.loader, parent=None),
                        "video": VideoController(self.loader, parent=None),
                        "convert": ConvertController(self.loader, parent=None),
                        "sample": SampleController(self.loader, parent=None),
                        "profile": ProfileController(self.loader, parent=None)}


    def __open(self, window):
        if self.children[window].ui.isHidden():
            if window == "sample":
                QtW.QApplication.instance().openSample.emit(-1)

            self.openWindow(self.children[window], fixed_size=window != "dataset")
        else:
            self.children[window].ui.activateWindow()

    def _connectUIBehavior(self):
        self.connect(self.ui.datasetBtn.clicked, lambda: self.__open("dataset"))
        self.connect(self.ui.imageBtn.clicked, lambda: self.__open("image"))
        self.connect(self.ui.bulkCaptionBtn.clicked, lambda: self.__open("bulk_caption"))
        self.connect(self.ui.videoBtn.clicked, lambda: self.__open("video"))
        self.connect(self.ui.convertBtn.clicked, lambda: self.__open("convert"))
        self.connect(self.ui.samplingBtn.clicked, lambda: self.__open("sample"))
        self.connect(self.ui.profilingBtn.clicked, lambda: self.__open("profile"))