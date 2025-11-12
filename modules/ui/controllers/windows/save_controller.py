from modules.ui.controllers.base_controller import BaseController

import PySide6.QtWidgets as QtW

from modules.ui.models.StateModel import StateModel

class SaveController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/save.ui", name=None, parent=parent)


    def connectUIBehavior(self):
        self.connect(self.ui.cancelBtn.clicked, lambda: self.ui.hide())
        self.connect(self.ui.okBtn.clicked, lambda: self.save())


    def save(self):
        name = self.ui.configCmb.currentText()
        if name != "" and not name.startswith("#"):
            StateModel.instance().save_to_file(name)

            QtW.QApplication.instance().stateChanged.emit()
            self.ui.hide()

            # TODO: SET PARENT configCmb TO NEWLY SAVED NAME -> Probably requires new global signal configChanged(idx) because at this point, parent configCmb has not yet updated the content.

        #else: # TODO: alert empty file, check existing files.
        #    pass