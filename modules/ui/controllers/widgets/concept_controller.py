from modules.ui.utils.base_controller import BaseController

from PySide6.QtCore import QCoreApplication as QCA


class ConceptController(BaseController):
    def __init__(self, loader, concept_window, idx, parent=None):
        super().__init__(loader, "modules/ui/views/widgets/concept.ui", name=None, parent=parent)

        self.concept_window = concept_window
        self.idx = idx

    # TODO: subclass QPushButton and promote conceptBtn to show the image
    # TODO: enableBtn text to concept name

    def connectUIBehavior(self):
        self.ui.conceptBtn.clicked.connect(lambda: self.__openConceptWindow())

    def __openConceptWindow(self):
        self.openWindow(self.concept_window, fixed_size=False)
        # TODO: pass to concept_window the state of the current concept