from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.ui.controllers.windows.concept_controller import ConceptController as WinConceptController
from modules.ui.controllers.widgets.concept_controller import ConceptController as WidgetConceptController

from modules.ui.models.ConceptModel import ConceptModel

import PySide6.QtWidgets as QtW

class ConceptsController(BaseController):
    children = []
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/concepts.ui", name=QCA.translate("main_window_tabs", "Concepts"), parent=parent)

        self.concept_window = WinConceptController(loader, parent=self)

        cb = self.__loadConfig()
        self.connect(self.ui.presetCmb.textActivated, cb)
        cb(self.ui.presetCmb.currentText())

        cb2 = self.__updateConcepts()  # Requires self.concept_window
        self.connect(QtW.QApplication.instance().conceptsChanged, cb2)
        self.connect(QtW.QApplication.instance().stateChanged, cb2)
        cb2()

    def connectUIBehavior(self):
        self.connect(self.ui.addConceptBtn.clicked, self.__appendConcept())


        self.connect(self.ui.disableConceptsBtn.clicked, self.__disableConcepts())

        cb = self.__updateConfigs()
        self.connect(QtW.QApplication.instance().stateChanged, cb)

        cb2 = self.__saveConfig()
        self.connect(QtW.QApplication.instance().aboutToQuit, cb2)
        self.connect(QtW.QApplication.instance().conceptsChanged, cb2)

        cb()

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
            ConceptModel.instance().delete_sample(idx)
            QtW.QApplication.instance().conceptsChanged.emit()

        return f

    # TODO: StateModel: concept_file_name
    # TODO: ConceptModel: ...

    # presetCmb -> Load/save json OK
    # addConceptBtn -> New concept OK
    # disableConceptsBtn -> Disable all concepts OK
    # listWidget -> Container

    # Child widget:
    # cloneBtn / deleteBtn -> clone/delete OK
    # conceptBtn -> Show image / open concept window / Emit openConcept(idx)
    # enableCbx -> Show name / Enable