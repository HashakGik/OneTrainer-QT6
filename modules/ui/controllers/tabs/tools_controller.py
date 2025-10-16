from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.controller_utils import AbstractController

from modules.ui.controllers.windows.dataset_controller import DatasetController
from modules.ui.controllers.windows.video_controller import VideoController
from modules.ui.controllers.windows.convert_controller import ConvertController
from modules.ui.controllers.windows.sample_controller import SampleController
from modules.ui.controllers.windows.profile_controller import ProfileController


class ToolsController(AbstractController):
    def __init__(self, loader, state=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/tools.ui", state=state, name=QCA.translate("main_window_tabs", "Tools"), parent=parent)


        self.children = {"dataset": DatasetController(loader, parent=None),
                        "video": VideoController(loader, parent=None),
                        "convert": ConvertController(loader, parent=None),
                        "sample": SampleController(loader, parent=None),
                        "profile": ProfileController(loader, parent=None)}


    def __open(self, window):
        if self.children[window].ui.isHidden():
            self.openWindow(self.children[window], fixed_size=window != "dataset")
        else:
            self.children[window].ui.activateWindow()

    def connectUIBehavior(self):
        self.ui.datasetBtn.clicked.connect(lambda: self.__open("dataset"))
        self.ui.videoBtn.clicked.connect(lambda: self.__open("video"))
        self.ui.convertBtn.clicked.connect(lambda: self.__open("convert"))
        self.ui.samplingBtn.clicked.connect(lambda: self.__open("sample"))
        self.ui.profilingBtn.clicked.connect(lambda: self.__open("profile"))