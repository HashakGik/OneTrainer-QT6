from PySide6.QtCore import QCoreApplication as QCA
from modules.ui.utils.base_controller import BaseController

from modules.ui.controllers.windows.concept_controller import ConceptController as WinConceptController
from modules.ui.controllers.widgets.concept_controller import ConceptController as WidgetConceptController


class ConceptsController(BaseController):
    def __init__(self, loader, parent=None):
        super().__init__(loader, "modules/ui/views/tabs/concepts.ui", name=QCA.translate("main_window_tabs", "Concepts"), parent=parent)

        self.concept_window = WinConceptController(loader, parent=self)
        self.children = {}

    def connectUIBehavior(self):
        self.ui.addConceptBtn.clicked.connect(lambda: self.__appendConcept())

    def __appendConcept(self):
        wdg = WidgetConceptController(self.loader, self.concept_window, len(self.children), parent=self)
        self.children[len(self.children)] = wdg
        #self._appendWidget(self.ui.listWidget, wdg, self_delete_fn=True, self_clone_fn=True)