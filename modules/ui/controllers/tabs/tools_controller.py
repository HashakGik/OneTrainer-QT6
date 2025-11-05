from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.ui.controllers.windows.dataset_controller import DatasetController
from modules.ui.controllers.windows.video_controller import VideoController
from modules.ui.controllers.windows.convert_controller import ConvertController
from modules.ui.controllers.windows.sample_controller import SampleController
from modules.ui.controllers.windows.profile_controller import ProfileController


class ToolsController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/tools.ui", state=state, mutex=mutex, name=QCA.translate("main_window_tabs", "Tools"), parent=parent)


        self.children = {"dataset": DatasetController(loader, parent=None, state=state, mutex=self.mutex),
                        "video": VideoController(loader, parent=None, state=state, mutex=self.mutex),
                        "convert": ConvertController(loader, parent=None, state=state, mutex=self.mutex),
                        "sample": SampleController(loader, parent=None, state=state, mutex=self.mutex),
                        "profile": ProfileController(loader, parent=None, state=state, mutex=self.mutex)}


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