from modules.ui.utils.base_controller import BaseController

from PySide6.QtCore import QCoreApplication as QCA
import PySide6.QtWidgets as QtW

from modules.ui.utils.ModelFlags import ModelFlags

class SaveController(BaseController):
    def __init__(self, loader, state=None, mutex=None, parent=None):
        super().__init__(loader, "modules/ui/views/windows/save.ui", state=state, mutex=mutex, name=None, parent=parent)


    def connectUIBehavior(self):
        self.ui.cancelBtn.clicked.connect(lambda: self.ui.hide())
        self.ui.okBtn.clicked.connect(lambda: self.save())


    def save(self):
        name = self.ui.configCmb.currentText()
        if name != "" and not name.startswith("#"):
            self.mutex.lock()
            self.parent._save_to_file(name)
            self.mutex.unlock()

            QtW.QApplication.instance().stateChanged.emit()
            self.ui.hide()
        #else: # TODO: alert empty file, check existing files.
        #    pass