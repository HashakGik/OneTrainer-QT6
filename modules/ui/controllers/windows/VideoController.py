from modules.ui.controllers.BaseController import BaseController

from PySide6.QtCore import QCoreApplication as QCA


class VideoController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/video.ui", name=None, parent=parent)

    def _connectUIBehavior(self):
        self._connectFileDialog(self.ui.linkListBtn, self.ui.linkListLed, is_dir=False, save=False,
                           title=QCA.translate("dialog_window", "Open Link list"),
                           filters=QCA.translate("filetype_filters",
                                                 "Text (*.txt)"))
        self._connectFileDialog(self.ui.singleVideo1Btn, self.ui.singleVideo1Led, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open Video"),
                               filters=QCA.translate("filetype_filters",
                                                     "Video (*.m4v, *.wmv, *.mp4, *.avi, *.webm)"))
        self._connectFileDialog(self.ui.singleVideo2Btn, self.ui.singleVideo2Led, is_dir=False, save=False,
                               title=QCA.translate("dialog_window", "Open Video"),
                               filters=QCA.translate("filetype_filters",
                                                     "Video (*.m4v, *.wmv, *.mp4, *.avi, *.webm)"))

        self._connectFileDialog(self.ui.directory1Btn, self.ui.directory1Led, is_dir=True, save=False,
                               title=QCA.translate("dialog_window", "Open Video directory"))
        self._connectFileDialog(self.ui.directory2Btn, self.ui.directory2Led, is_dir=True, save=False,
                               title=QCA.translate("dialog_window", "Open Video directory"))

        self._connectFileDialog(self.ui.output1Btn, self.ui.output1Led, is_dir=True, save=True,
                               title=QCA.translate("dialog_window", "Save Video directory"))
        self._connectFileDialog(self.ui.output2Btn, self.ui.output2Led, is_dir=True, save=True,
                               title=QCA.translate("dialog_window", "Save Video directory"))
        self._connectFileDialog(self.ui.output3Btn, self.ui.output3Led, is_dir=True, save=True,
                               title=QCA.translate("dialog_window", "Save Video directory"))

        self.connect(self.ui.infoBtn.clicked, lambda: self.openUrl("https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#usage-and-options"))