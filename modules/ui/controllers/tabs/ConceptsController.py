from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.controllers.BaseController import BaseController

from modules.ui.controllers.windows.ConceptController import ConceptController as WinConceptController
from modules.ui.controllers.widgets.ConceptController import ConceptController as WidgetConceptController

from modules.ui.models.ConceptModel import ConceptModel
from modules.ui.models.StateModel import StateModel

import PySide6.QtWidgets as QtW

class ConceptsController(BaseController):
    children = []
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/concepts.ui", name=QCA.translate("main_window_tabs", "Concepts"), parent=parent)

    def _setup(self):
        self.concept_window = WinConceptController(self.loader, parent=self)


    def _connectUIBehavior(self):
        self.connect(self.ui.addConceptBtn.clicked, self.__appendConcept())
        self.connect(self.ui.disableConceptsBtn.clicked, self.__disableConcepts())

        self.connect(QtW.QApplication.instance().stateChanged, self.__updateConfigs(), update_after_connect=True)

        cb2 = self.__saveConfig()
        self.connect(QtW.QApplication.instance().aboutToQuit, cb2)
        self.connect(QtW.QApplication.instance().conceptsChanged, cb2)

        self.connect(self.ui.presetCmb.textActivated, self.__loadConfig(), update_after_connect=True, initial_args=[self.ui.presetCmb.currentText()])

        cb4 = self.__updateConcepts()
        self.connect(QtW.QApplication.instance().conceptsChanged, cb4)
        self.connect(QtW.QApplication.instance().stateChanged, cb4, update_after_connect=True)


    def __updateConfigs(self):
        def f():
            configs = ConceptModel.instance().load_available_config_names("training_concepts", include_default=False)
            if len(configs) == 0:
                configs.append(("concepts", "training_concepts/concepts.json"))

            for c in self.children:
                c.disconnectAll()

            self.ui.presetCmb.clear()
            for k, v in configs:
                self.ui.presetCmb.addItem(k, userData=v)

            self.ui.presetCmb.setCurrentIndex(self.ui.presetCmb.findData(StateModel.instance().getState("concept_file_name")))
        return f

    def __loadConfig(self):
        def f(filename):
            ConceptModel.instance().load_config(filename)
            QtW.QApplication.instance().conceptsChanged.emit()
        return f

    def __saveConfig(self):
        def f():
            ConceptModel.instance().save_config()
        return f

    def __appendConcept(self):
        def f():
            ConceptModel.instance().create_new_concept()
            QtW.QApplication.instance().conceptsChanged.emit()
        return f

    def __disableConcepts(self):
        def f():
            ConceptModel.instance().disable_concepts()
            QtW.QApplication.instance().conceptsChanged.emit()
        return f

    def __updateConcepts(self):
        def f():
            for c in self.children:
                c.disconnectAll()

            self.ui.listWidget.clear()
            self.children = []

            for idx, _ in enumerate(ConceptModel.instance().getState("")):
               wdg = WidgetConceptController(self.loader, self.concept_window, idx, parent=self)
               self.children.append(wdg)
               self._appendWidget(self.ui.listWidget, wdg, self_delete_fn=self.__deleteConcept(idx), self_clone_fn=self.__cloneConcept(idx))

        return f

    def __cloneConcept(self, idx):
        def f():
            ConceptModel.instance().clone_concept(idx)
            QtW.QApplication.instance().conceptsChanged.emit()

        return f

    def __deleteConcept(self, idx):
        def f():
            ConceptModel.instance().delete_concept(idx)
            QtW.QApplication.instance().conceptsChanged.emit()

        return f