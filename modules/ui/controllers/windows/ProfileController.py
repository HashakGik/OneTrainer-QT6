from modules.ui.controllers.BaseController import BaseController

from modules.ui.models.StateModel import StateModel

from PySide6.QtCore import QCoreApplication as QCA

class ProfileController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/windows/profile.ui", name=None, parent=parent)

    def _connectUIBehavior(self):
        self.connect(self.ui.dumpBtn.clicked, self.__dump())
        self.connect(self.ui.startBtn.clicked, self.__toggleProfiling())

    def __dump(self):
        def f():
            StateModel.instance().dump_stack()
        return f

    def __toggleProfiling(self):
        def f():
            StateModel.instance().toggle_profiler()
            if StateModel.instance().is_profiling:
                self.ui.statusLbl.setText(QCA.translate("profiling_window", "Profiling active..."))
                self.ui.startBtn.setText(QCA.translate("profiling_window", "End Profiling"))
            else:
                self.ui.statusLbl.setText(QCA.translate("profiling_window", "Inactive"))
                self.ui.startBtn.setText(QCA.translate("profiling_window", "Start Profiling"))
        return f