from PySide6.QtCore import QCoreApplication as QCA

from modules.ui.controllers.BaseController import BaseController

from modules.util.enum.BulkEditMode import BulkEditMode

from modules.ui.models.BulkModel import BulkModel
from modules.ui.utils.WorkerPool import WorkerPool

class BulkCaptionController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/bulk_caption.ui", name=None, parent=parent)


    def _connectUIBehavior(self):
        self._connectFileDialog(self.ui.directoryBtn, self.ui.directoryLed, is_dir=True, save=False, title=
        QCA.translate("dialog_window", "Open Dataset directory"))

        state_ui_connections = {
            "directory": "directoryLed",
            "add_text": "addLed",
            "add_mode": "addCmb",
            "remove_text": "removeLed",
            "replace_text": "replaceLed",
            "replace_with": "replaceWithLed",
            "regex_pattern": "regexLed",
            "regex_replace": "regexWithLed",
        }

        self._connectStateUi(state_ui_connections, BulkModel.instance(), update_after_connect=True)
        self.connect(self.ui.applyBtn.clicked, self.__startProcessFiles(read_only=False))
        self.connect(self.ui.previewBtn.clicked, self.__startProcessFiles(read_only=True))

        self.__enableControls(True)()

    def __processFiles(self, read_only):
        def f(progress_fn=None):
            return BulkModel.instance().bulk_edit(read_only=read_only, preview_n=10, progress_fn=progress_fn)

        return f

    def __updateStatus(self):
        def f(data):
            if "status" in data:
                self.ui.statusLbl.setText(data["status"])

            if "data" in data:
                self.ui.previewTed.setPlainText(data["data"])
        return f

    def __startProcessFiles(self, read_only):
        def f():
            worker, name = WorkerPool.instance().createNamed(self.__processFiles(read_only), "process_bulk_captions", inject_progress_callback=True)
            worker.connect(init_fn=self.__enableControls(False), result_fn=None,
                           finished_fn=self.__enableControls(True),
                           errored_fn=self.__enableControls(True), aborted_fn=self.__enableControls(True),
                           progress_fn=self.__updateStatus())
            WorkerPool.instance().start(name)

        return f

    def __enableControls(self, enabled):
        def f():
            self.ui.applyBtn.setEnabled(enabled)
            self.ui.previewBtn.setEnabled(enabled)
        return f

    def _loadPresets(self):
        for e in BulkEditMode.enabled_values():
            self.ui.addCmb.addItem(e.pretty_print(), userData=e)